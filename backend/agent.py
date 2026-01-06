"""
AI Agent with RAG Capabilities for Free Tier

This module implements an AI agent that works on the free tier by using local processing
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

                # Re-try to get the embedding for the fallback HTTP approach
                query_embedding = self._get_embedding(query)

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
        Get embedding for text using Cohere with exponential backoff
        This method uses only Cohere embeddings with retry logic, no fallback
        """
        # Try Cohere with exponential backoff
        import cohere
        import time
        import random

        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise Exception("COHERE_API_KEY environment variable not set")

        co = cohere.Client(cohere_api_key)

        # Exponential backoff: 1s -> 2s -> 4s -> 8s -> 16s
        delays = [1, 2, 4, 8, 16]

        for attempt in range(5):  # Max 5 retries
            try:
                response = co.embed(
                    texts=[text],
                    model="embed-english-v3.0",
                    input_type="search_query"
                )
                logger.info(f"Cohere embedding succeeded on attempt {attempt + 1}")
                return response.embeddings[0]
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e) or "rate limit" in str(e).lower():
                    if attempt < len(delays):  # Still have delays to use
                        delay = delays[attempt]
                        jitter = random.uniform(0, 0.1 * delay)  # Add jitter
                        actual_delay = delay + jitter
                        logger.warning(f"Cohere rate limit hit on attempt {attempt + 1}, waiting {actual_delay:.2f}s: {str(e)}")
                        time.sleep(actual_delay)
                    else:
                        # No more retries left
                        raise Exception(f"Cohere embedding failed after 5 attempts with rate limits: {str(e)}")
                else:
                    # Not a rate limit error, re-raise immediately
                    raise Exception(f"Cohere embedding failed with non-rate-limit error: {str(e)}")

        # If we get here, all retries were exhausted
        raise Exception("Cohere embedding failed after maximum retries")


class RAGAgent:
    """
    Main RAG Agent class that works on the free tier using local processing
    """

    def __init__(self):
        self.retrieval_service = QdrantRetrievalService()
        logger.info("Free Tier RAG Agent initialized successfully")

    def generate_response(self, query: str, retrieved_chunks: List[RetrievedChunk]) -> str:
        """
        Generate a response based on the query and retrieved chunks using focused extraction
        This is a local implementation that doesn't require external API calls
        """
        # Limit to top 3 chunks to improve speed
        limited_chunks = retrieved_chunks[:3]

        # Extract relevant information from chunks based on the query
        relevant_parts = []

        # Normalize the query for better matching
        query_lower = query.lower()
        query_words = set(query_lower.split())

        for chunk in limited_chunks:
            # Look for parts of the chunk that are most relevant to the query
            text = chunk.text
            if len(text.strip()) == 0:
                continue

            # Simple keyword matching to extract relevant sentences
            sentences = text.split('. ')

            # Score each sentence based on how many query terms it contains
            sentence_scores = []
            for i, sentence in enumerate(sentences):
                sentence_lower = sentence.lower()
                # Count how many query terms appear in the sentence
                matches = sum(1 for term in query_words if term in sentence_lower and len(term) > 1)
                sentence_scores.append((matches, i, sentence.strip()))

            # Sort sentences by score (descending) and take top ones
            sentence_scores.sort(key=lambda x: x[0], reverse=True)

            relevant_sentences = []
            for score, idx, sentence in sentence_scores:
                if score > 0:  # At least one match
                    relevant_sentences.append(sentence)
                    if len(relevant_sentences) >= 2 or score >= 2:  # Take max 2 sentences or if highly relevant
                        break

            if relevant_sentences:
                relevant_parts.append('. '.join(relevant_sentences) + '.')
                break  # Take only from the first chunk that has matches

        # Combine relevant parts
        if relevant_parts:
            response_text = " ".join(relevant_parts).strip()
            # Limit response length to avoid overly long answers
            if len(response_text) > 300:
                response_text = response_text[:300] + "..."
            return response_text
        else:
            # If no direct matches, return a summary of the most relevant chunk
            if retrieved_chunks:
                most_relevant = retrieved_chunks[0]
                text = most_relevant.text
                if len(text) > 200:
                    text = text[:200] + "..."
                return f"Based on the knowledge base: {text}"
            else:
                return "I cannot find that information in the knowledge base."

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

            # Generate response using local processing (no external API calls)
            content = self.generate_response(user_query, retrieved_chunks)

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
        agent = RAGAgent()

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