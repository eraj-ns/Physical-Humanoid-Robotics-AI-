"""
Test script for the Free Tier RAG Agent to demonstrate functionality without external API calls
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from agent import RAGAgent

def test_free_tier_agent():
    print("Initializing Free Tier RAG Agent...")

    try:
        # Initialize the agent
        agent = RAGAgent()

        print("Free Tier RAG Agent initialized successfully!")
        print("Testing with sample queries...\n")

        # Test queries
        test_queries = [
            "What is ROS 2?",
            "Explain robotics concepts",
            "Tell me about AI and robotics"
        ]

        for query in test_queries:
            print(f"Query: {query}")
            response = agent.query(query)
            print(f"Response: {response.content}")
            print(f"Confidence: {response.confidence}")
            if response.sources:
                print(f"Sources ({len(response.sources)}):")
                for i, source in enumerate(response.sources[:2], 1):  # Show top 2 sources
                    print(f"  {i}. {source['url'][:50]}...")
            print("-" * 70)

    except Exception as e:
        print(f"Error running Free Tier RAG agent: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_free_tier_agent()