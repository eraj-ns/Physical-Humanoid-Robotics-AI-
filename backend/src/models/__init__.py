"""
Data models for the book embedding ingestion pipeline.
"""
from .data_models import DocumentationChunk, EmbeddingVector, SourceMetadata

__all__ = ["DocumentationChunk", "EmbeddingVector", "SourceMetadata"]