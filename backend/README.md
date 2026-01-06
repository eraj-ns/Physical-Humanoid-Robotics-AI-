# RAG Retrieval Pipeline Validation Tool

A Python script to connect to Qdrant and validate the RAG retrieval pipeline by:
1. Connecting to Qdrant and loading stored vectors
2. Accepting test queries and performing top-k similarity search
3. Validating results using returned text, metadata, and source URLs

## Prerequisites

- Python 3.11+
- Qdrant vector database with existing book content embeddings
- Cohere API key for embedding generation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   ```bash
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=your_collection_name
   COHERE_API_KEY=your_cohere_api_key
   ```

## Usage

### Test Qdrant Connection
```bash
python backend/retrieve.py --test-connection
```

### Process a Single Query
```bash
python backend/retrieve.py --query "your query here" --collection "collection_name" --top-k 5
```

### Process Batch Queries
```bash
python backend/retrieve.py --batch-queries "query1,query2,query3" --collection "collection_name" --top-k 5
```

### Run End-to-End Validation
```bash
python backend/retrieve.py --validate --query "test query" --collection "collection_name"
```

### Run Edge Case Validation
```bash
python backend/retrieve.py --validate-edge-cases --collection "collection_name"
```

### Run Batch Validation
```bash
python backend/retrieve.py --batch-validate "query1,query2,query3" --collection "collection_name"
```

## Environment Variables

- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for your Qdrant instance
- `QDRANT_COLLECTION_NAME`: Name of the collection to query (default: rag-chatbot-hackathon)
- `COHERE_API_KEY`: Your Cohere API key for embeddings

## Features

- Connect to Qdrant vector database and validate collection access
- Convert text queries to embeddings using Cohere
- Perform top-k similarity search against Qdrant collection
- Retrieve and display text chunks with metadata and source URLs
- Batch processing for multiple queries
- End-to-end validation of the retrieval pipeline
- Response time metrics collection
- Edge case validation (empty results, invalid parameters, etc.)
- Comprehensive error handling with logging