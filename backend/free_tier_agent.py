"""
AI Agent with RAG Capabilities using Local Models for Free Tier

This module implements an AI agent that works on the free tier by using local models
and avoiding paid API calls. It integrates with Qdrant search logic to retrieve
book content and responds using only retrieved information.
"""
import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import json

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Response from the AI agent"""
    content: str
    sources: List[Dict[str, Any]]
    confidence: str
    follow_up_questions: Optional[List[str]] = None


@dataclass
class RetrievedChunk:
    """A chunk of content retrieved from the knowledge base"""
    id: str
    text: str
    score: float
    source_url: str
    metadata: Dict[str, Any]


class QdrantRetrievalService:
    """
    Service to retrieve information from Qdrant database.
    Reuses existing retrieval logic from retrieve.py.
    """

    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "rag-chatbot-hackathon")

        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")

        from qdrant_client import QdrantClient
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            timeout=10.0
        )

        logger.info(f"Qdrant client initialized for collection: {self.collection_name}")

    def retrieve_chunks(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks from Qdrant based on the query.
        """
        try:
            # First, convert the query to an embedding using the local method
            query_embedding = self._get_embedding(query)

            # Perform the search using the query embedding (using newer query_points API)
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            # Format the results
            retrieved_chunks = []
            for result in search_results.points:
                chunk = RetrievedChunk(
                    id=result.id,
                    text=result.payload.get('text', ''),
                    score=result.score,
                    source_url=result.payload.get('source_url', ''),
                    metadata=result.payload
                )
                retrieved_chunks.append(chunk)

            logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: {query[:50]}...")
            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error retrieving chunks from Qdrant: {str(e)}")
            # Try the HTTP API approach as fallback
            try:
                import requests
                headers = {
                    "Content-Type": "application/json",
                    "api-key": self.qdrant_api_key
                }

                search_payload = {
                    "vector": query_embedding,
                    "limit": top_k,
                    "with_payload": True,
                    "with_vectors": False
                }

                response = requests.post(
                    f"{self.qdrant_url}/collections/{self.collection_name}/points/search",
                    headers=headers,
                    json=search_payload
                )

                if response.status_code == 200:
                    results = response.json()
                    retrieved_chunks = []
                    for result in results.get("result", []):
                        chunk = RetrievedChunk(
                            id=result.get("id"),
                            text=result.get("payload", {}).get('text', ''),
                            score=result.get("score"),
                            source_url=result.get("payload", {}).get('source_url', ''),
                            metadata=result.get("payload", {})
                        )
                        retrieved_chunks.append(chunk)

                    logger.info(f"Retrieved {len(retrieved_chunks)} chunks via HTTP API for query: {query[:50]}...")
                    return retrieved_chunks
                else:
                    logger.error(f"HTTP search failed: {response.status_code} - {response.text}")
                    return []
            except Exception as fallback_e:
                logger.error(f"Fallback retrieval also failed: {str(fallback_e)}")
                return []

    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using Cohere or fallback to local embeddings
        This method reuses the logic from retrieve.py
        """
        # Try Cohere first
        try:
            import cohere
            cohere_api_key = os.getenv("COHERE_API_KEY")
            if cohere_api_key:
                co = cohere.Client(cohere_api_key)
                response = co.embed(
                    texts=[text],
                    model="embed-english-v3.0",
                    input_type="search_query"
                )
                return response.embeddings[0]
        except Exception as e:
            logger.warning(f"Cohere embedding failed: {str(e)}, falling back to local embeddings")

        # Fallback to local embeddings
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = model.encode([text])[0].tolist()

            # Pad or truncate to match expected dimension (1024 to match Cohere)
            if len(embedding) < 1024:
                # Pad with zeros to reach 1024 dimensions
                embedding.extend([0.0] * (1024 - len(embedding)))
            elif len(embedding) > 1024:
                # Truncate to 1024 dimensions
                embedding = embedding[:1024]

            return embedding
        except Exception as e:
            logger.error(f"Local embedding failed: {str(e)}")
            # Return a zero vector as fallback with correct dimensions
            return [0.0] * 1024


class FreeTierRAGAgent:
    """
    Main RAG Agent class that works on the free tier using local processing
    """

    def __init__(self):
        self.retrieval_service = QdrantRetrievalService()
        logger.info("Free Tier RAG Agent initialized successfully")

    def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response based on the query and context using simple rules
        This is a local implementation that doesn't require external API calls
        """
        # Simple rule-based response generation for free tier
        # In a real implementation, you might use a local LLM like transformers
        response_parts = []

        # Check if we have relevant information
        if context.strip():
            response_parts.append(f"Based on the retrieved information:")
            response_parts.append("")
            response_parts.append(context)
            response_parts.append("")
            response_parts.append(f"For your query '{query}', here's what I found in the knowledge base.")
        else:
            response_parts.append("I cannot find that information in the knowledge base.")

        return "\n".join(response_parts)

    async def query_async(self, user_query: str) -> AgentResponse:
        """
        Process a user query asynchronously and return a response based on retrieved information
        """
        logger.info(f"Processing query: {user_query}")

        try:
            # First, retrieve relevant information from Qdrant
            retrieved_chunks = self.retrieval_service.retrieve_chunks(user_query)

            if not retrieved_chunks:
                logger.warning("No relevant information found in knowledge base")
                return AgentResponse(
                    content="I cannot find that information in the knowledge base.",
                    sources=[],
                    confidence="low"
                )

            # Format the retrieved information for the agent
            retrieved_content = "\n\n".join([
                f"Source: {chunk.source_url}\nContent: {chunk.text[:500]}"  # Limit to 500 chars to keep it concise
                for chunk in retrieved_chunks
            ])

            # Generate response using local processing (no external API calls)
            content = self.generate_response(user_query, retrieved_content)

            # Format the sources
            sources = [
                {"id": chunk.id, "url": chunk.source_url, "text": chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text}
                for chunk in retrieved_chunks
            ]

            # Determine confidence based on retrieval results
            confidence = "high" if retrieved_chunks and len(retrieved_chunks) > 0 else "low"

            logger.info(f"Query processed successfully. Response length: {len(content)}")
            return AgentResponse(
                content=content,
                sources=sources,
                confidence=confidence
            )

        except Exception as e:
            logger.error(f"Error in query processing: {str(e)}")
            return AgentResponse(
                content="Sorry, I encountered an error processing your request.",
                sources=[],
                confidence="low"
            )

    def query(self, user_query: str) -> AgentResponse:
        """
        Process a user query and return a response based on retrieved information
        This is a synchronous wrapper around the async method
        """
        return asyncio.run(self.query_async(user_query))


def main():
    """
    Main function to demonstrate the free tier RAG agent
    """
    print("Initializing Free Tier RAG Agent...")

    try:
        # Initialize the agent
        agent = FreeTierRAGAgent()

        print("Free Tier RAG Agent initialized successfully!")
        print("You can now ask questions about the book content.")
        print("Type 'quit' to exit.\n")

        while True:
            user_input = input("Your question: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Process the query
            response = agent.query(user_input)

            print(f"\nResponse: {response.content}")
            if response.sources:
                print(f"\nSources ({len(response.sources)}):")
                for i, source in enumerate(response.sources[:3], 1):  # Show top 3 sources
                    print(f"  {i}. {source['url'][:50]}...")
                    print(f"     Preview: {source['text'][:100]}...")
            else:
                print("\nNo sources found in knowledge base.")
            print(f"Confidence: {response.confidence}\n")
            print("-" * 70)

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        logger.error(f"Error running RAG agent: {str(e)}")
        print(f"Error running RAG agent: {str(e)}")


if __name__ == "__main__":
    main()