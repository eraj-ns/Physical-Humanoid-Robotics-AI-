"""
Test script to simulate curl request to the FastAPI RAG integration
"""
import subprocess
import json
import time
import threading
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from api import app
import uvicorn

def run_server():
    """Run the FastAPI server in a separate thread for testing"""
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

def test_api_with_requests():
    """Test the API using requests library to simulate curl"""
    print("Starting server in background...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Give the server a moment to start
    time.sleep(3)

    print("Testing API with requests...")

    # Test the query endpoint
    try:
        response = requests.post(
            "http://localhost:8001/query",
            json={"query": "What is ROS 2?"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response Content Length: {len(data['content'])}")
            print(f"Number of Sources: {len(data['sources'])}")
            print(f"Confidence: {data['confidence']}")
            print("SUCCESS: API is working correctly!")
        else:
            print(f"ERROR: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Is it running on port 8000?")
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out.")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_api_with_requests()