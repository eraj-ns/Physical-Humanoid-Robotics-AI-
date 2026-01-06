"""
Robust RAG Retrieval System with API Rate Limit Protection and Local Embeddings Fallback

This module implements a comprehensive RAG (Retrieval Augmented Generation) system that:
1. Handles API rate limits gracefully
2. Provides local embeddings as fallback
3. Verifies data exists in Qdrant
4. Retrieves top-k relevant documents
5. Builds context and answers questions using only retrieved data
"""
import os
import logging
import sys
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import time
import requests
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_retrieval.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """Result of a retrieval operation"""
    success: bool
    documents: List[Dict[str, Any]]
    query_embedding: List[float]
    retrieval_time: float
    error_message: Optional[str] = None


@dataclass
class RAGResponse:
    """Final RAG response"""
    retrieval_status: str
    answer: str
    retrieved_documents: List[Dict[str, Any]]
    retrieval_time: float


class LocalEmbeddingService:
    """
    Local embedding service using sentence-transformers as fallback.
    This avoids API rate limits and provides reliable embedding generation.
    """

    def __init__(self):
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the local embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            # Using a lightweight but effective model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Local embedding model initialized successfully")
        except ImportError:
            logger.warning("sentence-transformers not installed. Install with: pip install sentence-transformers")
            logger.info("Falling back to dummy embeddings - please install sentence-transformers for proper local embeddings")
            self.model = None
        except Exception as e:
            logger.error(f"Failed to initialize local embedding model: {str(e)}")
            self.model = None

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text using local model"""
        try:
            # Ensure text is not empty
            if not text or not text.strip():
                text = "empty text"

            if self.model is None:
                # Return a simple dummy embedding when model is not available
                logger.warning("Local embedding model not available, using dummy embedding")
                return [0.0] * 384  # all-MiniLM-L6-v2 outputs 384-dimensional vectors

            # Generate embedding
            embedding = self.model.encode([text])[0].tolist()
            return embedding
        except Exception as e:
            logger.error(f"Error generating local embedding: {str(e)}")
            # Return a zero vector as fallback
            return [0.0] * 384  # all-MiniLM-L6-v2 outputs 384-dimensional vectors

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            if self.model is None:
                # Return dummy embeddings when model is not available
                logger.warning("Local embedding model not available, using dummy embeddings")
                return [[0.0] * 384 for _ in texts]

            # Filter out empty texts
            clean_texts = [text if text.strip() else "empty text" for text in texts]
            embeddings = self.model.encode(clean_texts).tolist()
            return embeddings
        except Exception as e:
            logger.error(f"Error generating local embeddings: {str(e)}")
            # Return zero vectors as fallback
            return [[0.0] * 384 for _ in texts]


class CohereEmbeddingService:
    """
    Cohere embedding service with rate limit handling.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required")

        self.base_url = "https://api.cohere.ai/v1/embed"
        self.model = "embed-english-v3.0"
        self.input_type = "search_query"
        self._last_request_time = 0
        self._min_request_interval = 1.0  # Minimum 1 second between requests

    def _rate_limit_delay(self):
        """Implement basic rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time

        if time_since_last_request < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last_request
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def generate_embedding(self, text: str, max_retries: int = 3) -> Optional[List[float]]:
        """Generate embedding for a single text using Cohere API with retry and exponential backoff"""
        for attempt in range(max_retries):
            try:
                self._rate_limit_delay()

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "texts": [text],
                    "model": self.model,
                    "input_type": self.input_type
                }

                response = requests.post(self.base_url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    embeddings = data.get("embeddings", [])
                    if embeddings and len(embeddings) > 0:
                        return embeddings[0]
                    else:
                        logger.error("No embeddings returned from Cohere API")
                        return None
                elif response.status_code == 429:  # Rate limit
                    logger.warning(f"Cohere API rate limit exceeded (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:  # If not the last attempt
                        # Exponential backoff: wait 2^attempt seconds
                        wait_time = 2 ** attempt
                        logger.info(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error("Cohere API rate limit exceeded after all retries")
                        return None
                else:
                    logger.error(f"Cohere API error: {response.status_code} - {response.text}")
                    if response.status_code == 429 and attempt < max_retries - 1:
                        # Exponential backoff for rate limit
                        wait_time = 2 ** attempt
                        logger.info(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    return None

            except Exception as e:
                logger.error(f"Error calling Cohere API: {str(e)}")
                if attempt < max_retries - 1:
                    # Exponential backoff for other errors too
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                return None

        return None


class QdrantClient:
    """
    Qdrant client for vector database operations with proper error handling.
    """

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, collection_name: Optional[str] = None):
        self.url = url or os.getenv("QDRANT_URL")
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION_NAME", "rag-chatbot-hackathon")

        if not self.url:
            raise ValueError("QDRANT_URL is required")
        if not self.api_key:
            raise ValueError("QDRANT_API_KEY is required")

        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

    def verify_connection(self) -> bool:
        """Verify connection to Qdrant"""
        try:
            response = requests.get(f"{self.url}/collections", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {str(e)}")
            return False

    def collection_exists(self) -> bool:
        """Check if the specified collection exists"""
        try:
            response = requests.get(f"{self.url}/collections/{self.collection_name}", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error checking collection existence: {str(e)}")
            return False

    def get_collection_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the collection"""
        try:
            response = requests.get(f"{self.url}/collections/{self.collection_name}", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return None

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform similarity search in Qdrant"""
        try:
            search_payload = {
                "vector": query_vector,
                "limit": top_k,
                "with_payload": True,
                "with_vectors": False
            }

            response = requests.post(
                f"{self.url}/collections/{self.collection_name}/points/search",
                headers=self.headers,
                json=search_payload
            )

            if response.status_code == 200:
                results = response.json()
                return results.get("result", [])
            else:
                logger.error(f"Qdrant search failed: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error performing Qdrant search: {str(e)}")
            return []


class RobustRAGSystem:
    """
    Robust RAG system with fallback mechanisms and rate limit protection.
    """

    def __init__(self):
        self.qdrant_client = QdrantClient()
        self.cohere_service = None
        self.local_service = None
        self._initialize_embedding_services()

    def _initialize_embedding_services(self):
        """Initialize both Cohere and local embedding services"""
        # Initialize Cohere service if API key is available
        try:
            self.cohere_service = CohereEmbeddingService()
        except ValueError:
            logger.warning("Cohere API key not available, will use local embeddings only")

        # Always initialize local service as fallback
        try:
            self.local_service = LocalEmbeddingService()
        except ImportError:
            logger.error("Could not initialize local embedding service. Please install sentence-transformers.")
            raise

    def _get_embedding(self, text: str) -> Tuple[List[float], str]:
        """
        Get embedding using Cohere first, fall back to local sentence-transformers if needed.
        Returns embedding vector and source ('cohere' or 'local').
        """
        # Try Cohere first if available
        if self.cohere_service:
            cohere_embedding = self.cohere_service.generate_embedding(text, max_retries=3)
            if cohere_embedding is not None:
                logger.info("Using Cohere embedding service")
                return cohere_embedding, "cohere"
            else:
                logger.warning("Cohere embedding failed, falling back to local embeddings")

        # Fall back to local embedding
        logger.info("Using local embedding service as fallback")
        local_embedding = self.local_service.generate_embedding(text)
        return local_embedding, "local"

    def verify_data_exists(self) -> bool:
        """Verify that data exists in Qdrant"""
        if not self.qdrant_client.verify_connection():
            logger.error("Cannot connect to Qdrant")
            return False

        if not self.qdrant_client.collection_exists():
            logger.error(f"Collection '{self.qdrant_client.collection_name}' does not exist")
            return False

        collection_info = self.qdrant_client.get_collection_info()
        if collection_info:
            points_count = collection_info.get("result", {}).get("points_count", 0)
            if points_count == 0:
                logger.warning(f"Collection '{self.qdrant_client.collection_name}' exists but is empty")
                return False
            else:
                logger.info(f"Collection has {points_count} points")
                return True

        return False

    def retrieve_documents(self, query: str, top_k: int = 5) -> RetrievalResult:
        """Retrieve top-k documents from Qdrant"""
        start_time = time.time()

        try:
            # Get embedding for the query
            query_embedding, embedding_source = self._get_embedding(query)

            if not query_embedding or len(query_embedding) == 0:
                return RetrievalResult(
                    success=False,
                    documents=[],
                    query_embedding=[],
                    retrieval_time=time.time() - start_time,
                    error_message="Failed to generate query embedding"
                )

            # Perform search in Qdrant
            search_results = self.qdrant_client.search(query_embedding, top_k)

            if not search_results:
                return RetrievalResult(
                    success=False,
                    documents=[],
                    query_embedding=query_embedding,
                    retrieval_time=time.time() - start_time,
                    error_message="No documents found in Qdrant"
                )

            # Format results
            documents = []
            for result in search_results:
                document = {
                    "id": result.get("id"),
                    "score": result.get("score"),
                    "text": result.get("payload", {}).get("text", ""),
                    "source_url": result.get("payload", {}).get("source_url", ""),
                    "metadata": result.get("payload", {}),
                    "embedding_source": embedding_source
                }
                documents.append(document)

            retrieval_time = time.time() - start_time
            logger.info(f"Retrieved {len(documents)} documents in {retrieval_time:.2f}s")

            return RetrievalResult(
                success=True,
                documents=documents,
                query_embedding=query_embedding,
                retrieval_time=retrieval_time
            )

        except Exception as e:
            logger.error(f"Error in retrieve_documents: {str(e)}")
            return RetrievalResult(
                success=False,
                documents=[],
                query_embedding=[],
                retrieval_time=time.time() - start_time,
                error_message=str(e)
            )

    def build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        if not documents:
            return ""

        context_parts = []
        for i, doc in enumerate(documents, 1):
            text = doc.get("text", "")
            source = doc.get("source_url", "Unknown source")
            score = doc.get("score", 0)

            context_part = f"Document {i} (Relevance: {score:.3f}, Source: {source}):\n{text}\n"
            context_parts.append(context_part)

        return "\n".join(context_parts)

    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using only the provided context"""
        if not context.strip():
            return "Information not found in the knowledge base."

        # Simple approach: return relevant information from context
        # In a real implementation, you might use a language model here
        # For now, we'll just return the context as the answer
        return context

    def query(self, user_query: str, top_k: int = 5) -> RAGResponse:
        """Main query method that orchestrates the entire RAG process"""
        start_time = time.time()

        # Verify data exists in Qdrant
        if not self.verify_data_exists():
            return RAGResponse(
                retrieval_status="failure",
                answer="Information not found in the knowledge base.",
                retrieved_documents=[],
                retrieval_time=time.time() - start_time
            )

        # Retrieve documents
        retrieval_result = self.retrieve_documents(user_query, top_k)

        if not retrieval_result.success:
            logger.error(f"Retrieval failed: {retrieval_result.error_message}")
            return RAGResponse(
                retrieval_status="failure",
                answer="Information not found in the knowledge base.",
                retrieved_documents=[],
                retrieval_time=time.time() - start_time
            )

        # Build context from retrieved documents
        context = self.build_context(retrieval_result.documents)

        # Generate answer using context
        answer = self.generate_answer(user_query, context)

        total_time = time.time() - start_time

        return RAGResponse(
            retrieval_status="success",
            answer=answer,
            retrieved_documents=retrieval_result.documents,
            retrieval_time=total_time
        )


def main(user_query: str):
    """
    Main function to execute the RAG retrieval process.
    """
    logger.info(f"Starting RAG retrieval for query: {user_query}")

    try:
        # Initialize the robust RAG system
        rag_system = RobustRAGSystem()

        # Execute the query
        result = rag_system.query(user_query, top_k=5)

        # Output results
        print(f"\nRetrieval Status: {result.retrieval_status}")
        print(f"Retrieval Time: {result.retrieval_time:.2f}s")
        print(f"\nAnswer:\n{result.answer}")

        if result.retrieved_documents:
            print(f"\nRetrieved {len(result.retrieved_documents)} documents:")
            for i, doc in enumerate(result.retrieved_documents, 1):
                print(f"  {i}. Score: {doc['score']:.3f}, Source: {doc['source_url'][:50]}...")

        return result

    except Exception as e:
        logger.error(f"Error in main RAG process: {str(e)}")
        print(f"Retrieval Status: failure")
        print(f"Error: {str(e)}")
        return RAGResponse(
            retrieval_status="failure",
            answer="Information not found in the knowledge base.",
            retrieved_documents=[],
            retrieval_time=0
        )


if __name__ == "__main__":
    # Get user query from command line or use default
    import sys
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = "What is this documentation about?"  # Default query

    main(user_query)