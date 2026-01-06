# RAG System for Docusaurus Documentation

This project implements a Retrieval-Augmented Generation (RAG) system that crawls Docusaurus documentation sites, generates embeddings using Cohere, and stores them in Qdrant for efficient retrieval.

## Features

- Crawls Docusaurus documentation sites automatically
- Extracts and cleans text content from pages
- Chunks text with configurable size and overlap
- Generates embeddings using Cohere's models
- Stores embeddings in Qdrant vector database
- Provides vector search functionality

## Prerequisites

- Python 3.8+
- Cohere API key
- Qdrant Cloud account (or local instance)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env` and fill in your configuration:
   ```bash
   cp .env.example .env
   ```
3. Update the `.env` file with your API keys and URLs

## Configuration

The system is configured via the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant instance URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `DOCUSAURUS_BASE_URL`: The base URL of the Docusaurus site to crawl
- `CHUNK_SIZE`: Size of text chunks (default: 512)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)

## Usage

### Run the full pipeline

```bash
python -m src.main
```

This will:
1. Crawl the Docusaurus site
2. Extract and clean content
3. Chunk the text
4. Generate embeddings
5. Store embeddings in Qdrant

### Test the search functionality

```bash
python -m src.search
```

This will run sample searches against your vector database.

### Run the test pipeline

```bash
python test_pipeline.py
```

This runs a complete test of all components with a small sample.