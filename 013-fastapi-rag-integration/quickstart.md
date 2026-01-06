# Quickstart: FastAPI RAG Integration

## Prerequisites

- Python 3.11+
- pip package manager
- Existing environment with RAG agent dependencies installed

## Setup

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Ensure existing dependencies are installed**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (if not already done):
   ```bash
   # Create .env file with required variables:
   QDRANT_URL="your_qdrant_url"
   QDRANT_API_KEY="your_qdrant_api_key"
   QDRANT_COLLECTION_NAME="rag-chatbot-hackathon"
   COHERE_API_KEY="your_cohere_api_key"  # Optional, for fallback
   ```

## Running the API Server

1. **Start the FastAPI server**:
   ```bash
   cd backend
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify the server is running**:
   - Open your browser to `http://localhost:8000/docs` to see the automatic API documentation
   - The API endpoint will be available at `http://localhost:8000/query`

## Testing the API

### Using curl:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"query": "What is ROS 2?"},
    headers={"Content-Type": "application/json"}
)

print(response.json())
```

## API Usage

### Request Format
```json
{
  "query": "Your question here"
}
```

### Response Format
```json
{
  "content": "The answer from the RAG agent",
  "sources": [
    {
      "id": "document_id",
      "url": "https://source-url.com",
      "text": "Preview of the source content..."
    }
  ],
  "confidence": "high",
  "follow_up_questions": ["Suggested follow-up question 1", "Suggested follow-up question 2"]
}
```

## Error Handling

- **400 Bad Request**: Query is invalid or missing required fields
- **500 Internal Server Error**: An error occurred during query processing

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.