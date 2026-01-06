# Local Embeddings Setup Guide

This guide explains how to set up local embeddings as the default option to avoid API rate limits in your RAG system.

## Why Use Local Embeddings?

- **No rate limits**: Local embeddings don't depend on external APIs
- **Cost effective**: No per-token charges
- **Privacy**: Data never leaves your system
- **Reliability**: Not affected by API outages

## Installation

### 1. Install Required Dependencies

```bash
pip install sentence-transformers torch
```

### 2. Verify Installation

```bash
python -c "from sentence_transformers import SentenceTransformer; print('Local embeddings ready!')"
```

## Configuration

### Option 1: Modify Environment Variables

Set these in your `.env` file to prefer local embeddings:

```env
# Remove or comment out COHERE_API_KEY to force local embeddings
# COHERE_API_KEY=your_key_here

# Keep Qdrant settings
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=rag-chatbot-hackathon
```

### Option 2: Update Code to Prioritize Local Embeddings

In your application, you can modify the priority to use local embeddings first:

```python
# In rag_retrieval.py, you can adjust the _get_embedding method to prefer local:
def _get_embedding(self, text: str) -> Tuple[List[float], str]:
    """
    Get embedding using local first (faster and no rate limits),
    fall back to Cohere if local is not available.
    Returns embedding vector and source ('local' or 'cohere').
    """
    # Try local first (faster and no rate limits)
    if self.local_service:
        try:
            local_embedding = self.local_service.generate_embedding(text)
            # Check if it's a dummy embedding (all zeros)
            if local_embedding and any(val != 0.0 for val in local_embedding):
                logger.info("Using local embedding service")
                return local_embedding, "local"
        except Exception as e:
            logger.warning(f"Local embedding failed: {str(e)}, falling back to Cohere")

    # Fall back to Cohere if local failed or not available
    if self.cohere_service:
        cohere_embedding = self.cohere_service.generate_embedding(text, max_retries=3)
        if cohere_embedding is not None:
            logger.info("Using Cohere embedding service")
            return cohere_embedding, "cohere"

    # Final fallback - return dummy embedding
    logger.error("Both local and Cohere embedding services failed, using dummy embedding")
    return [0.0] * 384, "dummy"
```

## Recommended Local Models

The current implementation uses `all-MiniLM-L6-v2`, which is:
- Fast and lightweight
- Good performance for most use cases
- 384-dimensional vectors

Alternative models you can use:
- `all-mpnet-base-v2` - Higher quality, slower (768-dimensional)
- `paraphrase-multilingual-MiniLM-L12-v2` - Good for multilingual content

## Performance Comparison

| Option | Speed | Cost | Reliability | Quality |
|--------|-------|------|-------------|---------|
| Local (all-MiniLM-L6-v2) | Fast | Free | High | Good |
| Cohere | Fast | Per-token | Medium | High |
| OpenAI | Medium | Per-token | Medium | High |

## Troubleshooting

### If you get memory errors with local embeddings:
```python
# Use a smaller model or limit batch size
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # Smaller model
```

### If local embeddings are too slow:
- Consider using a faster model like `all-MiniLM-L12-v2`
- Use GPU acceleration if available: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

## Best Practices

1. **Always have a fallback**: The system should work even if local embeddings fail
2. **Monitor performance**: Track embedding generation times
3. **Consider hybrid approach**: Use local for queries, Cohere for ingestion if needed
4. **Cache embeddings**: Store generated embeddings to avoid recomputation

## Complete Setup Command

```bash
# Install all required dependencies
pip install sentence-transformers torch qdrant-client cohere python-dotenv

# Verify setup
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(['test'])
print(f'Local embeddings working! Shape: {embedding.shape}')
"
```

Now your RAG system will primarily use local embeddings, falling back to Cohere only when needed, significantly reducing the chance of hitting API rate limits.