"""
Script to verify that the vectors were stored in the Qdrant collection
"""
from src.storage.qdrant_client import QdrantStorage
from src.config import Config
from src.utils import setup_logging


def verify_ingestion():
    """
    Verify that the vectors were stored in the Qdrant collection
    """
    logger = setup_logging(Config.LOG_LEVEL)

    # Connect to the same collection
    collection_name = "rag-chatbot-hackathon"
    qdrant_client = QdrantStorage(collection_name=collection_name)

    # Get collection info
    collection_info = qdrant_client.get_collection_info()

    print("\n" + "="*60)
    print("QDRANT COLLECTION VERIFICATION")
    print("="*60)

    if collection_info:
        print(f"Collection Name: {collection_info.get('name', 'Unknown')}")
        print(f"Vector Size: {collection_info.get('vector_size', 'Unknown')}")
        print(f"Distance: {collection_info.get('distance', 'Unknown')}")
        print(f"Point Count: {collection_info.get('point_count', 'Unknown')}")
    else:
        print("Could not retrieve collection info")

    # Try to get a few sample records to confirm they exist
    try:
        # Get a sample of points from the collection
        records = qdrant_client.client.scroll(
            collection_name=collection_name,
            limit=3  # Get first 3 records
        )

        print(f"\nSample records retrieved: {len(records[0])}")

        for i, record in enumerate(records[0][:3]):  # Show first 3 records
            payload = record.payload
            print(f"\nRecord {i+1}:")
            print(f"  ID: {record.id}")
            print(f"  URL: {payload.get('url', 'N/A')}")
            print(f"  Title: {payload.get('title', 'N/A')}")
            print(f"  Text preview: {payload.get('text', '')[:100]}...")

    except Exception as e:
        print(f"Error retrieving sample records: {str(e)}")

    print("="*60)


if __name__ == "__main__":
    print("Verifying Qdrant ingestion...")
    verify_ingestion()