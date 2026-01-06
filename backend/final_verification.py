"""
Final verification script for the FastAPI RAG integration
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from api import app, QueryRequest, AgentResponseModel
from fastapi.testclient import TestClient

def final_verification():
    print("=== Final Verification: FastAPI RAG Integration ===")

    # Create a test client
    client = TestClient(app)

    print("\n1. Testing server health...")
    response = client.get("/health")
    if response.status_code == 200:
        print("   SUCCESS: Health endpoint: OK")
    else:
        print(f"   ERROR: Health endpoint: FAILED ({response.status_code})")
        return False

    print("\n2. Testing root endpoint...")
    response = client.get("/")
    if response.status_code == 200:
        print("   SUCCESS: Root endpoint: OK")
    else:
        print(f"   ERROR: Root endpoint: FAILED ({response.status_code})")
        return False

    print("\n3. Testing query endpoint with valid query...")
    response = client.post("/query", json={"query": "What is ROS 2?"})
    if response.status_code == 200:
        data = response.json()
        print(f"   SUCCESS: Query endpoint: OK")
        print(f"   - Response length: {len(data['content'])} characters")
        print(f"   - Sources returned: {len(data['sources'])}")
        print(f"   - Confidence level: {data['confidence']}")
    else:
        print(f"   ERROR: Query endpoint: FAILED ({response.status_code}) - {response.text}")
        return False

    print("\n4. Testing error handling with empty query...")
    response = client.post("/query", json={"query": ""})
    if response.status_code == 400:
        print("   SUCCESS: Error handling: OK (properly rejects empty queries)")
    else:
        print(f"   ERROR: Error handling: FAILED ({response.status_code})")
        return False

    print("\n5. Testing request/response model validation...")
    try:
        # Test request model
        req = QueryRequest(query="test query")
        print("   SUCCESS: Request model: OK")

        # Test response model (using sample data)
        resp = AgentResponseModel(
            content="test content",
            sources=[{"id": "1", "url": "http://example.com", "text": "test text"}],
            confidence="high"
        )
        print("   SUCCESS: Response model: OK")
    except Exception as e:
        print(f"   ERROR: Model validation: FAILED ({str(e)})")
        return False

    print("\n=== VERIFICATION COMPLETE ===")
    print("SUCCESS: All tests passed!")
    print("SUCCESS: FastAPI RAG integration is working correctly")
    print("SUCCESS: API endpoints are functional")
    print("SUCCESS: Error handling is in place")
    print("SUCCESS: Request/response models are validated")
    print("\nThe FastAPI server is ready for frontend integration!")

    return True

if __name__ == "__main__":
    final_verification()