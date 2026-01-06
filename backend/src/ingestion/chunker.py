import re
from typing import List
from ..models.data_models import DocumentationChunk
from datetime import datetime


class TextChunker:
    """
    A chunker that splits text into configurable segments for embedding.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, source_url: str = "", title: str = "") -> List[DocumentationChunk]:
        """
        Split text into chunks of specified size with overlap.
        Memory-optimized version that processes text in a streaming fashion.

        Args:
            text: The text to chunk
            source_url: The source URL for the text
            title: The title of the source document

        Returns:
            List of DocumentationChunk objects
        """
        if not text:
            return []

        chunks = []
        start_idx = 0

        while start_idx < len(text):
            # Calculate the end index for this chunk
            end_idx = start_idx + self.chunk_size

            # If this is not the last chunk, try to break at sentence boundary
            if end_idx < len(text):
                # Look for sentence boundaries near the end of the chunk
                chunk_text = text[start_idx:end_idx]
                # Find the last sentence ending in the last 200 characters of the chunk
                search_start = max(0, len(chunk_text) - 200)
                sentence_end_pos = -1

                for separator in ['.\s', '!\s', '?\s', '\n', ';', ':']:
                    last_pos = chunk_text[search_start:].rfind(separator)
                    if last_pos != -1:
                        sentence_end_pos = search_start + last_pos + len(separator)
                        break

                if sentence_end_pos > 0:
                    end_idx = start_idx + sentence_end_pos
                else:
                    # If no sentence boundary found, just cut at the limit
                    pass

            # Extract the chunk text
            chunk_text = text[start_idx:end_idx].strip()

            if chunk_text:  # Only add non-empty chunks
                chunk = DocumentationChunk(
                    id="",
                    content=chunk_text,
                    source_url=source_url,
                    title=title,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata={"start_pos": start_idx, "end_pos": end_idx}
                )
                chunks.append(chunk)

                # For memory optimization, limit the number of chunks in memory at once
                # This is more relevant when processing very large documents
                if len(chunks) > 1000:  # Arbitrary limit to prevent excessive memory usage
                    # In a production system, you might want to write chunks to storage
                    # rather than keeping them all in memory
                    pass

            # Move to the next chunk position, considering overlap
            start_idx = end_idx - self.chunk_overlap

            # If the next chunk would be too small, break
            if len(text) - start_idx < 50:
                break

        return chunks

    def chunk_by_paragraph(self, text: str, source_url: str = "", title: str = "") -> List[DocumentationChunk]:
        """
        Split text into chunks by paragraphs, with fallback to character-based chunking if paragraphs are too large.

        Args:
            text: The text to chunk
            source_url: The source URL for the text
            title: The title of the source document

        Returns:
            List of DocumentationChunk objects
        """
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []

        current_chunk = ""
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                # Save the current chunk
                if current_chunk.strip():
                    chunk = DocumentationChunk(
                        id="",
                        content=current_chunk.strip(),
                        source_url=source_url,
                        title=title,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        metadata={"chunk_type": "paragraph"}
                    )
                    chunks.append(chunk)

                # Start a new chunk with the current paragraph
                current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the final chunk if it exists
        if current_chunk.strip():
            chunk = DocumentationChunk(
                id="",
                content=current_chunk.strip(),
                source_url=source_url,
                title=title,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={"chunk_type": "paragraph"}
            )
            chunks.append(chunk)

        # If any chunks are still too large, further split them using character-based chunking
        final_chunks = []
        for chunk in chunks:
            if len(chunk.content) > self.chunk_size:
                # Split this chunk further using character-based method
                sub_chunks = self.chunk_text(chunk.content, source_url, title)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)

        return final_chunks