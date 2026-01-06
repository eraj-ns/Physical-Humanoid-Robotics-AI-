from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict
from ..models.data_models import EmbeddingVector
from ..config import Config
from ..utils import setup_logging
import uuid


class QdrantStorage:
    """
    A wrapper for Qdrant vector database operations.
    """

    def __init__(self, url: str = None, api_key: str = None, collection_name: str = None):
        """
        Initialize the Qdrant storage client.

        Args:
            url: Qdrant URL. If None, uses the URL from configuration.
            api_key: Qdrant API key. If None, uses the key from configuration.
            collection_name: Name of the collection to use. If None, uses the name from configuration.
        """
        self.url = url or Config.QDRANT_URL
        self.api_key = api_key or Config.QDRANT_API_KEY
        self.collection_name = collection_name or Config.QDRANT_COLLECTION_NAME

        if not self.url:
            raise ValueError("Qdrant URL is required")

        # Initialize the Qdrant client
        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key,
            prefer_grpc=True  # Use gRPC for better performance if available
        )

        self.logger = setup_logging(Config.LOG_LEVEL)

    def create_collection(self, vector_size: int = 1024, distance: str = "Cosine") -> bool:
        """
        Create a collection in Qdrant for storing embeddings.

        Args:
            vector_size: Size of the embedding vectors (default 1024 for Cohere embeddings)
            distance: Distance metric to use for similarity search (Cosine, Euclid, Dot)

        Returns:
            True if collection was created successfully, False otherwise
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            existing_collection_names = [collection.name for collection in collections.collections]

            if self.collection_name in existing_collection_names:
                self.logger.info(f"Collection '{self.collection_name}' already exists")
                return True

            # Create the collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance[distance.upper()]
                )
            )

            self.logger.info(f"Collection '{self.collection_name}' created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error creating collection '{self.collection_name}': {str(e)}")
            return False

    def store_embeddings(self, embeddings: List[EmbeddingVector]) -> bool:
        """
        Store a list of embeddings in Qdrant.

        Args:
            embeddings: List of EmbeddingVector objects to store

        Returns:
            True if embeddings were stored successfully, False otherwise
        """
        if not embeddings:
            self.logger.warning("No embeddings to store")
            return True

        try:
            # Prepare points for insertion
            points = []
            for embedding in embeddings:
                # Create a unique ID if not provided
                point_id = str(uuid.uuid4()) if not embedding.id else embedding.id

                # Prepare the payload with metadata
                payload = {
                    "chunk_id": embedding.chunk_id,
                    "model_version": embedding.model_version,
                    "created_at": str(embedding.created_at) if hasattr(embedding, 'created_at') else ""
                }

                # Create a point for Qdrant
                point = models.PointStruct(
                    id=point_id,
                    vector=embedding.vector,
                    payload=payload
                )

                points.append(point)

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            self.logger.info(f"Stored {len(points)} embeddings in collection '{self.collection_name}'")
            return True
        except Exception as e:
            self.logger.error(f"Error storing embeddings: {str(e)}")
            return False

    def search_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar embeddings in Qdrant.

        Args:
            query_vector: The query embedding vector
            top_k: Number of top similar results to return

        Returns:
            List of dictionaries containing similar embeddings and their metadata
        """
        try:
            # Perform the search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )

            # Format the results
            results = []
            for result in search_results:
                result_dict = {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                    "vector": result.vector if result.vector else None
                }
                results.append(result_dict)

            return results
        except Exception as e:
            self.logger.error(f"Error searching for similar embeddings: {str(e)}")
            return []

    def validate_retrieval(self, test_query_vector: List[float], expected_chunk_ids: List[str] = None) -> Dict:
        """
        Validate that the vector search returns relevant chunks for test queries.

        Args:
            test_query_vector: A test query vector to use for validation
            expected_chunk_ids: Optional list of expected chunk IDs that should be returned

        Returns:
            Dictionary with validation results
        """
        try:
            # Perform a search with the test query
            results = self.search_similar(test_query_vector, top_k=5)

            validation_result = {
                "success": True,
                "retrieved_count": len(results),
                "results": results
            }

            # If expected chunk IDs are provided, validate them
            if expected_chunk_ids:
                retrieved_chunk_ids = [result["payload"].get("chunk_id") for result in results if "payload" in result]
                matches = [chunk_id for chunk_id in retrieved_chunk_ids if chunk_id in expected_chunk_ids]

                validation_result["expected_matches"] = len(matches)
                validation_result["expected_match_ratio"] = len(matches) / len(expected_chunk_ids) if expected_chunk_ids else 0
                validation_result["matched_chunk_ids"] = matches

            self.logger.info(f"Retrieved {len(results)} results for test query")
            return validation_result
        except Exception as e:
            self.logger.error(f"Error validating retrieval: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def delete_collection(self) -> bool:
        """
        Delete the collection from Qdrant.

        Returns:
            True if collection was deleted successfully, False otherwise
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            self.logger.info(f"Collection '{self.collection_name}' deleted successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting collection '{self.collection_name}': {str(e)}")
            return False

    def get_collection_info(self) -> Optional[Dict]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information or None if error
        """
        try:
            collection_info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "point_count": collection_info.points_count
            }
        except Exception as e:
            self.logger.error(f"Error getting collection info: {str(e)}")
            return None

    def ping(self) -> bool:
        """
        Test the connection to Qdrant.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to get collections to test the connection
            self.client.get_collections()
            return True
        except Exception as e:
            self.logger.error(f"Error connecting to Qdrant: {str(e)}")
            return False