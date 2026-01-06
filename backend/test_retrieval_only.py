"""
Test script to verify the Qdrant retrieval functionality works properly
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from agent import QdrantRetrievalService

def test_retrieval():
    print("Testing Qdrant retrieval functionality...")

    try:
        # Initialize the retrieval service
        retrieval_service = QdrantRetrievalService()

        # Test queries
        test_queries = [
            "What is ROS 2?",
            "Explain robotics concepts",
            "Tell me about AI and robotics"
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            chunks = retrieval_service.retrieve_chunks(query, top_k=3)
            print(f"Retrieved {len(chunks)} chunks:")
            for i, chunk in enumerate(chunks, 1):
                print(f"  {i}. Score: {chunk.score:.3f}")
                print(f"     Source: {chunk.source_url[:50]}...")
                print(f"     Text preview: {chunk.text[:100]}...")
                print()

        print("SUCCESS: Retrieval functionality is working correctly!")

    except Exception as e:
        print(f"ERROR: Error in retrieval: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_retrieval()