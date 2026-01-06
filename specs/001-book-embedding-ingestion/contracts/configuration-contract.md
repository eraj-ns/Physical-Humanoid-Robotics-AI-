# Configuration Contract: Book Embedding Ingestion Pipeline

## Purpose
This contract defines the expected configuration parameters for the book embedding ingestion pipeline. The system expects these parameters to be available as environment variables or through a configuration file.

## Configuration Schema

### Required Parameters
- `COHERE_API_KEY` (string)
  - Description: API key for accessing Cohere embedding services
  - Format: Alphanumeric string with dashes
  - Example: `your-cohere-api-key-here`

- `QDRANT_URL` (string)
  - Description: URL endpoint for the Qdrant vector database
  - Format: Valid HTTP/HTTPS URL
  - Example: `https://your-cluster.us-east.qdrant.io:6333`

- `QDRANT_API_KEY` (string)
  - Description: API key for accessing Qdrant database
  - Format: Alphanumeric string
  - Example: `your-qdrant-api-key-here`

### Optional Parameters
- `QDRANT_COLLECTION_NAME` (string)
  - Description: Name of the collection in Qdrant to store embeddings
  - Default: `docs_embeddings`
  - Format: Valid collection name (alphanumeric with underscores/dashes)
  - Example: `documentation_chunks`

- `DOCUMENTATION_URLS` (string)
  - Description: Comma-separated list of documentation URLs to crawl
  - Default: `""`
  - Format: Comma-separated valid URLs
  - Example: `https://docs.example.com,https://guide.example.com`

- `CHUNK_SIZE` (integer)
  - Description: Size of text chunks in characters
  - Default: `1000`
  - Format: Positive integer
  - Example: `1000`

- `CHUNK_OVERLAP` (integer)
  - Description: Overlap between chunks in characters
  - Default: `200`
  - Format: Non-negative integer
  - Example: `200`

- `EMBEDDING_MODEL` (string)
  - Description: Name of the Cohere embedding model to use
  - Default: `embed-english-v3.0`
  - Format: Valid Cohere model name
  - Example: `embed-english-v3.0`

## Expected Input Format
The pipeline accepts configuration through environment variables or a `.env` file. The system will validate that all required parameters are present before starting the ingestion process.

## Expected Output Format
The pipeline will output:
- Processed documentation chunks stored in Qdrant with associated metadata
- Log messages indicating the status of each processing step
- Error messages if any step fails

## Error Handling Contract
- If required parameters are missing, the system will raise a ConfigurationError
- If URL crawling fails, the system will log the error and continue with other URLs
- If embedding generation fails, the system will retry up to 3 times before skipping the chunk
- If Qdrant storage fails, the system will log the error and continue processing other chunks