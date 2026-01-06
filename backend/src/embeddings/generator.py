import cohere
from typing import List, Dict
from ..models.data_models import DocumentationChunk, EmbeddingVector
from ..config import Config
from ..utils import setup_logging
import time
import sys
from datetime import datetime, timedelta
import threading


class CohereEmbeddingService:
    """
    Service for generating embeddings using Cohere's API.
    """

    def __init__(self, api_key: str = None, model: str = None, requests_per_minute: int = 10):
        """
        Initialize the Cohere embedding service.

        Args:
            api_key: Cohere API key. If None, uses the key from configuration.
            model: Cohere model to use. If None, uses the model from configuration.
            requests_per_minute: Maximum number of requests allowed per minute
        """
        self.api_key = api_key or Config.COHERE_API_KEY
        self.model = model or Config.EMBEDDING_MODEL
        self.requests_per_minute = requests_per_minute

        if not self.api_key:
            raise ValueError("Cohere API key is required")

        # Validate the API key before initializing the client
        if not self._validate_api_key():
            raise ValueError("Invalid Cohere API key")

        # Initialize rate limiting variables
        self._request_times = []
        self._lock = threading.Lock()

        self.client = cohere.Client(self.api_key)
        self.logger = setup_logging(Config.LOG_LEVEL)

    def _validate_api_key(self) -> bool:
        """
        Validate the Cohere API key by making a simple API call.

        Returns:
            True if the API key is valid, False otherwise
        """
        try:
            # Try to make a simple call to validate the API key
            # We'll call the embed method with a dummy request
            dummy_response = self.client.embed(
                texts=["test"],
                model=self.model,
                input_type="search_document"
            )
            return True
        except Exception as e:
            self.logger.error(f"Error validating Cohere API key: {str(e)}")
            return False

    def _enforce_rate_limit(self):
        """
        Enforce rate limiting to respect the maximum requests per minute.
        """
        with self._lock:
            now = datetime.now()
            # Remove requests older than 1 minute
            self._request_times = [
                req_time for req_time in self._request_times
                if now - req_time < timedelta(minutes=1)
            ]

            # If we've reached the limit, wait until we're under the limit
            if len(self._request_times) >= self.requests_per_minute:
                # Wait until the oldest request is older than 1 minute
                wait_time = 60 - (now - self._request_times[0]).total_seconds()
                if wait_time > 0:
                    time.sleep(wait_time)
                    # After waiting, update the list again
                    now = datetime.now()
                    self._request_times = [
                        req_time for req_time in self._request_times
                        if now - req_time < timedelta(minutes=1)
                    ]

            # Record this request
            self._request_times.append(now)

    def _generate_batch_embeddings(self, texts: List[str], max_retries: int = 3) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts with retry logic and rate limiting.

        Args:
            texts: List of texts to generate embeddings for
            max_retries: Maximum number of retry attempts

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        # Enforce rate limiting before making the API call
        self._enforce_rate_limit()

        for attempt in range(max_retries):
            try:
                response = self.client.embed(
                    texts=texts,
                    model=self.model,
                    input_type="search_document"  # Using search_document for documentation content
                )
                return response.embeddings
            except cohere.CohereError as e:
                # Check if it's a rate limit error
                if "rate limit" in str(e).lower():
                    self.logger.warning(f"Rate limit exceeded, waiting before retry...")
                    # Wait longer for rate limit errors
                    time.sleep(60)
                    continue

                self.logger.warning(f"Cohere API error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to generate embeddings after {max_retries} attempts: {str(e)}")
                    # Return empty embeddings for failed texts
                    return [None for _ in texts]
                else:
                    # Wait before retrying (exponential backoff)
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
            except Exception as e:
                self.logger.error(f"Unexpected error generating embeddings: {str(e)}")
                return [None for _ in texts]

        return [None for _ in texts]

    def generate_embeddings(self, texts: List[str], max_retries: int = 3) -> List[EmbeddingVector]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to generate embeddings for
            max_retries: Maximum number of retry attempts for API calls

        Returns:
            List of EmbeddingVector objects
        """
        if not texts:
            return []

        embeddings = []
        batch_size = 96  # Cohere's recommended batch size is 96

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self._generate_batch_embeddings(batch, max_retries)

            # Create EmbeddingVector objects for each embedding
            for idx, embedding_vector in enumerate(batch_embeddings):
                if embedding_vector is not None:
                    embedding = EmbeddingVector(
                        id="",
                        vector=embedding_vector,
                        chunk_id=f"chunk_{i + idx}",  # This will be updated with actual chunk ID later
                        model_version=self.model
                    )
                    embeddings.append(embedding)

        return embeddings

    def _generate_batch_embeddings(self, texts: List[str], max_retries: int = 3) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts with retry logic.

        Args:
            texts: List of texts to generate embeddings for
            max_retries: Maximum number of retry attempts

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        for attempt in range(max_retries):
            try:
                response = self.client.embed(
                    texts=texts,
                    model=self.model,
                    input_type="search_document"  # Using search_document for documentation content
                )
                return response.embeddings
            except cohere.CohereError as e:
                self.logger.warning(f"Cohere API error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to generate embeddings after {max_retries} attempts: {str(e)}")
                    # Return empty embeddings for failed texts
                    return [None for _ in texts]
                else:
                    # Wait before retrying (exponential backoff)
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
            except Exception as e:
                self.logger.error(f"Unexpected error generating embeddings: {str(e)}")
                return [None for _ in texts]

        return [None for _ in texts]

    def generate_embedding_for_chunks(self, chunks: List[DocumentationChunk]) -> List[EmbeddingVector]:
        """
        Generate embeddings for a list of DocumentationChunk objects.

        Args:
            chunks: List of DocumentationChunk objects

        Returns:
            List of EmbeddingVector objects with proper chunk_id references
        """
        if not chunks:
            return []

        # Extract text content from chunks
        texts = [chunk.content for chunk in chunks]

        # Generate embeddings
        embeddings = self.generate_embeddings(texts)

        # Update the chunk_id in embeddings to match the actual chunk IDs
        for i, embedding in enumerate(embeddings):
            if embedding is not None and i < len(chunks):
                embedding.chunk_id = chunks[i].id

        return embeddings

    def validate_embedding_dimensions(self, embeddings: List[EmbeddingVector]) -> bool:
        """
        Validate that all embeddings have the correct dimensions for the model.

        Args:
            embeddings: List of EmbeddingVector objects to validate

        Returns:
            True if all embeddings have correct dimensions, False otherwise
        """
        if not embeddings:
            return True

        # Get expected dimensions for the model (this is based on Cohere's documentation)
        expected_dims = self._get_expected_dimensions()
        if expected_dims <= 0:
            # If we can't determine expected dimensions, just return True
            return True

        for embedding in embeddings:
            if len(embedding.vector) != expected_dims:
                self.logger.error(f"Embedding has {len(embedding.vector)} dimensions, expected {expected_dims}")
                return False

        return True

    def _get_expected_dimensions(self) -> int:
        """
        Get the expected dimensions for the current model.

        Returns:
            Expected number of dimensions, or 0 if unknown
        """
        # Based on Cohere documentation, different models have different dimensions
        # embed-english-v3.0 has 1024 dimensions for search_document input type
        if "embed-english-v3.0" in self.model.lower():
            return 1024
        elif "embed-multilingual-v3.0" in self.model.lower():
            return 1024
        elif "embed-english-light-v3.0" in self.model.lower():
            return 384
        elif "embed-multilingual-light-v3.0" in self.model.lower():
            return 384
        else:
            # For other models, we'll assume 1024 as a common default
            # In a real implementation, you might want to call the API to get model info
            return 1024