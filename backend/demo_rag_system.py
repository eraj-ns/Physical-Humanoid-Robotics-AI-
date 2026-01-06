"""
Example script to demonstrate the complete RAG solution.
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

from rag_retrieval import RobustRAGSystem

# Load environment variables
load_dotenv()

def demo_rag_system():
    """Demonstrate the complete RAG system functionality"""

    print("Initializing Robust RAG System...")
    print("="*50)

    try:
        # Initialize the RAG system
        rag_system = RobustRAGSystem()

        # Verify data exists
        print("Verifying data exists in Qdrant...")
        if not rag_system.verify_data_exists():
            print("No data found in Qdrant. Please ensure your data has been ingested.")
            return

        print("Data verification successful!")
        print()

        # Example queries
        example_queries = [
            "What is this documentation about?",
            "Tell me about the key features",
            "How does the system work?"
        ]

        for i, query in enumerate(example_queries, 1):
            print(f"Query {i}: {query}")
            print("-" * 30)

            # Execute the query
            result = rag_system.query(query, top_k=3)

            print(f"Retrieval Status: {result.retrieval_status}")
            print(f"Retrieval Time: {result.retrieval_time:.2f}s")
            print(f"Answer:\n{result.answer}")

            if result.retrieved_documents:
                print(f"Retrieved {len(result.retrieved_documents)} documents:")
                for j, doc in enumerate(result.retrieved_documents, 1):
                    print(f"  {j}. Score: {doc['score']:.3f}")
                    print(f"     Source: {doc['source_url'][:60]}...")
                    print(f"     Preview: {doc['text'][:100]}...")
                    print()

            print("="*50)
            print()

    except Exception as e:
        print(f"Error in RAG system: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main function to run the RAG system demo"""
    print("Robust RAG System - Complete Solution")
    print()

    # Check if required environment variables are set
    required_vars = ["QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"⚠️  Missing required environment variables: {missing_vars}")
        print("Please set them in your .env file")
        return

    demo_rag_system()

if __name__ == "__main__":
    main()