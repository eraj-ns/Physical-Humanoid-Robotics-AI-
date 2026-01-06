# Data Model: RAG Retrieval Pipeline Validation

## Vector Embeddings
- **Description**: Numerical representations of text chunks from book content, stored in Qdrant for semantic search
- **Fields**:
  - `id`: Unique identifier for the embedding record
  - `vector`: Array of float values representing the embedding
  - `payload`: Dictionary containing metadata including:
    - `text`: The original text chunk
    - `source_url`: URL where the original content was found
    - `metadata`: Additional information about the source

## Query
- **Description**: User input text that will be converted to an embedding for similarity search
- **Fields**:
  - `text`: The query text string
  - `top_k`: Number of results to return (default: 5)
  - `query_embedding`: Vector representation of the query text

## Retrieval Results
- **Description**: Top-k text chunks returned based on semantic similarity to the query
- **Fields**:
  - `points`: Array of Point objects from Qdrant containing:
    - `id`: ID of the matching vector
    - `score`: Similarity score
    - `payload`: Metadata dictionary with text, source_url, and additional metadata
  - `query`: Original query text
  - `top_k`: Number of results requested

## Validation Result
- **Description**: Result of validation checks on retrieved content
- **Fields**:
  - `is_valid`: Boolean indicating if validation passed
  - `retrieved_chunks`: List of retrieved text chunks
  - `source_urls`: List of source URLs from metadata
  - `metadata_consistency`: Boolean indicating if metadata is consistent
  - `relevance_score`: Estimated relevance of results to query