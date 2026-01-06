"""
Script to verify that data exists in Qdrant collection.
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_qdrant_data():
    """Verify that data exists in the Qdrant collection"""

    # Get configuration from environment
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "rag-chatbot-hackathon")

    if not qdrant_url:
        print("Error: QDRANT_URL environment variable is not set")
        return False

    if not qdrant_api_key:
        print("Error: QDRANT_API_KEY environment variable is not set")
        return False

    headers = {
        "Content-Type": "application/json",
        "api-key": qdrant_api_key
    }

    try:
        # Test connection
        print(f"Connecting to Qdrant at: {qdrant_url}")
        response = requests.get(f"{qdrant_url}/collections", headers=headers)

        if response.status_code != 200:
            print(f"Failed to connect to Qdrant: {response.status_code} - {response.text}")
            return False

        print("Successfully connected to Qdrant")

        # Check if collection exists
        print(f"Checking for collection: {collection_name}")
        response = requests.get(f"{qdrant_url}/collections/{collection_name}", headers=headers)

        if response.status_code != 200:
            print(f"Collection '{collection_name}' does not exist")
            collections_response = requests.get(f"{qdrant_url}/collections", headers=headers)
            if collections_response.status_code == 200:
                available_collections = collections_response.json()
                print(f"Available collections: {[coll['name'] for coll in available_collections.get('collections', [])]}")
            return False

        print("Collection exists")

        # Get collection info
        collection_info = response.json()
        points_count = collection_info.get("result", {}).get("points_count", 0)
        vector_size = collection_info.get("result", {}).get("config", {}).get("params", {}).get("vectors", {}).get("size", "Unknown")

        print(f"Collection info:")
        print(f"  - Points count: {points_count}")
        print(f"  - Vector size: {vector_size}")

        if points_count == 0:
            print("Collection exists but is empty")
            return False

        # Get a sample of points to verify they contain data
        print("\nRetrieving sample points to verify data...")
        search_response = requests.post(
            f"{qdrant_url}/collections/{collection_name}/points/scroll",
            headers=headers,
            json={"limit": 3, "with_payload": True, "with_vectors": False}
        )

        if search_response.status_code == 200:
            sample_data = search_response.json()
            points = sample_data.get("result", {}).get("points", [])

            if points:
                print(f"Found {len(points)} sample points with data:")
                for i, point in enumerate(points, 1):
                    payload = point.get("payload", {})
                    text_preview = payload.get("text", "")[:100] + "..." if len(payload.get("text", "")) > 100 else payload.get("text", "")
                    print(f"  Point {i}:")
                    print(f"    ID: {point.get('id')}")
                    print(f"    Text preview: {text_preview}")
                    print(f"    Source: {payload.get('source_url', 'N/A')}")
                    print()
            else:
                print("⚠ No points returned in sample")
                return False
        else:
            print(f"Failed to retrieve sample points: {search_response.status_code} - {search_response.text}")
            return False

        print("Data verification successful - Qdrant collection contains data")
        return True

    except Exception as e:
        print(f"Error verifying Qdrant data: {str(e)}")
        return False

if __name__ == "__main__":
    print("Verifying Qdrant data existence...")
    success = verify_qdrant_data()

    if success:
        print("\nVerification complete: Data exists in Qdrant")
    else:
        print("\nVerification failed: No data found in Qdrant")