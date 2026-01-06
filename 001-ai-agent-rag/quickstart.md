# Quickstart: AI Agent with RAG Capabilities

## Prerequisites

- Python 3.11+
- OpenAI API key
- Qdrant database with book content
- Environment variables configured:
  - `OPENAI_API_KEY`: Your OpenAI API key
  - `QDRANT_URL`: URL to your Qdrant instance
  - `QDRANT_API_KEY`: API key for Qdrant access
  - `QDRANT_COLLECTION_NAME`: Name of the collection containing book content (default: rag-chatbot-hackathon)

## Setup

1. **Install Dependencies**
   ```bash
   pip install openai qdrant-client python-dotenv
   ```

2. **Configure Environment**
   Create a `.env` file in your project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=rag-chatbot-hackathon
   ```

3. **Verify Qdrant Connection**
   Ensure your Qdrant instance is running and contains the expected book content.

## Running the Agent

1. **Create the agent.py file** in the backend directory:
   ```bash
   # The agent will be created in backend/agent.py
   ```

2. **Run the agent**:
   ```bash
   cd backend
   python agent.py
   ```

3. **Interact with the agent**:
   - The agent will initialize and be ready to accept queries
   - Type your questions about the book content
   - The agent will retrieve relevant information and respond using only the retrieved content

## Example Usage

```python
# Initialize the agent
from agent import RAGAgent

# Create agent instance
agent = RAGAgent()

# Ask a question
response = agent.query("What are the key concepts in Chapter 1?")
print(response.content)
print("Sources:", response.sources)
```

## Expected Output

The agent will respond to queries with:
- Answers based only on retrieved content
- Source citations for the information provided
- Clear indication when information is not available in the knowledge base
- Support for follow-up questions maintaining conversation context

## Troubleshooting

- **API Connection Issues**: Verify your OpenAI and Qdrant API keys are correct
- **No Results**: Check that your Qdrant collection contains the expected content
- **Slow Responses**: Verify that your Qdrant instance is properly configured and indexed