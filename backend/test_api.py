"""
Test script for the FastAPI RAG integration
"""
import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from api import app, QueryRequest
from fastapi.testclient import TestClient

def test_api():
    # Create a test client
    client = TestClient(app)

    print("Testing the FastAPI RAG integration...")

    # Test the root endpoint
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint response: {response.json()}")

    # Test the health endpoint
    response = client.get("/health")
    print(f"Health endpoint status: {response.status_code}")
    print(f"Health endpoint response: {response.json()}")

    # Test the query endpoint
    test_query = {"query": "What is ROS 2?"}
    response = client.post("/query", json=test_query)
    print(f"Query endpoint status: {response.status_code}")

    if response.status_code == 200:
        response_data = response.json()
        print(f"Query response content length: {len(response_data.get('content', ''))}")
        print(f"Number of sources: {len(response_data.get('sources', []))}")
        print(f"Confidence level: {response_data.get('confidence')}")
        print("Query endpoint working correctly!")
    else:
        print(f"Query endpoint error: {response.json()}")

    # Test with empty query (should return 400)
    empty_query = {"query": ""}
    response = client.post("/query", json=empty_query)
    print(f"Empty query status: {response.status_code}")
    if response.status_code == 400:
        print("Proper error handling for empty queries!")
    else:
        print(f"Unexpected response for empty query: {response.json()}")

if __name__ == "__main__":
    test_api()