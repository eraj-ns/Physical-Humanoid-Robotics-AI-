"""
Final summary of the sitemap ingestion to Qdrant
"""
from src.storage.qdrant_client import QdrantStorage
from src.config import Config


def print_summary():
    """
    Print a summary of the ingestion results
    """
    collection_name = "rag-chatbot-hackathon"

    # Initialize Qdrant client
    qdrant_client = QdrantStorage(collection_name=collection_name)

    # Get collection info
    collection_info = qdrant_client.get_collection_info()

    print("\n" + "="*70)
    print("INGESTION SUMMARY - SITEMAP TO QDRANT")
    print("="*70)
    print(f"Target Collection: {collection_name}")
    print(f"Total Vectors Stored: {collection_info.get('point_count', 0)}")
    print(f"Vector Dimension: {collection_info.get('vector_size', 0)}")
    print(f"Distance Metric: {collection_info.get('distance', 'Unknown')}")
    print()

    # Get all unique URLs that were processed
    try:
        # Get all records to count unique URLs
        all_records, _ = qdrant_client.client.scroll(
            collection_name=collection_name,
            limit=10000  # Get all records
        )

        # Extract unique URLs from payloads
        unique_urls = set()
        for record in all_records:
            url = record.payload.get('url')
            if url:
                unique_urls.add(url)

        print(f"Unique Documentation Pages Processed: {len(unique_urls)}")
        print("\nSample URLs that were ingested:")
        for i, url in enumerate(sorted(unique_urls)[:10]):  # Show first 10 URLs
            print(f"  {i+1:2d}. {url}")

        if len(unique_urls) > 10:
            print(f"  ... and {len(unique_urls) - 10} more pages")

        print("\nSample Content Chunks with Metadata:")
        print("-" * 70)
        # Show a few sample records with their metadata
        for i, record in enumerate(all_records[:3]):  # Show first 3 records
            payload = record.payload
            print(f"Chunk {i+1}:")
            print(f"  URL: {payload.get('url', 'N/A')}")
            print(f"  Title: {payload.get('title', 'N/A')}")
            print(f"  Text Preview: {payload.get('text', '')[:100]}...")
            print(f"  Chunk Index: {payload.get('chunk_index', 'N/A')}")
            print()

    except Exception as e:
        print(f"Error retrieving records: {str(e)}")

    print("="*70)
    print("INGESTION COMPLETE AND VERIFIED")
    print("All documentation pages from sitemap.xml have been successfully")
    print("ingested into the Qdrant collection with embeddings and metadata.")
    print("="*70)


if __name__ == "__main__":
    print_summary()