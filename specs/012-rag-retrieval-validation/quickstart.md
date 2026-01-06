# Quickstart: RAG Retrieval Pipeline Validation

## Overview
This guide explains how to set up and run the RAG retrieval validation script to test your Qdrant vector database with Cohere embeddings.

## Prerequisites
- Python 3.11 or higher
- Qdrant vector database with existing book content embeddings
- Cohere API key for embedding generation
- Python packages: `qdrant-client`, `cohere`

## Setup

1. **Install Dependencies**:
   ```bash
   pip install qdrant-client cohere
   ```

2. **Set Environment Variables**:
   ```bash
   export QDRANT_URL="your-qdrant-url"
   export QDRANT_API_KEY="your-qdrant-api-key"
   export COHERE_API_KEY="your-cohere-api-key"
   export QDRANT_COLLECTION_NAME="your-collection-name"
   ```

3. **Prepare Your Qdrant Collection**:
   - Ensure your Qdrant instance has a collection with vector embeddings
   - Verify the collection contains metadata with text chunks and source URLs

## Usage

1. **Run Basic Validation**:
   ```bash
   python backend/retrieve.py --query "your test query here"
   ```

2. **Run Batch Validation**:
   ```bash
   python backend/retrieve.py --batch-queries "query1,query2,query3" --top-k 5
   ```

3. **Validate Specific Collection**:
   ```bash
   python backend/retrieve.py --query "test query" --collection "my_collection" --top-k 10
   ```

## Configuration Options

- `--query`: Single query to test against the RAG system
- `--batch-queries`: Comma-separated list of queries for batch validation
- `--top-k`: Number of results to retrieve (default: 5)
- `--collection`: Qdrant collection name (default: environment variable)
- `--validate`: Run validation checks on retrieved results (default: true)

## Example

```bash
# Validate RAG retrieval with a sample query
python backend/retrieve.py --query "What are the key concepts in machine learning?" --top-k 3

# Output will include:
# - Retrieved text chunks
# - Source URLs
# - Similarity scores
# - Validation results
```

## Troubleshooting

- **Connection Issues**: Verify QDRANT_URL and QDRANT_API_KEY are set correctly
- **Empty Results**: Check that your Qdrant collection has embeddings stored
- **API Errors**: Ensure COHERE_API_KEY is valid and you have sufficient quota