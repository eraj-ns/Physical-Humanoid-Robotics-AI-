import unittest
from src.ingestion.chunker import TextChunker
from src.models.data_models import DocumentationChunk


class TestTextChunker(unittest.TestCase):
    """
    Unit tests for the TextChunker class.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.chunker = TextChunker(chunk_size=100, chunk_overlap=20)

    def test_chunk_text_basic(self):
        """Test basic text chunking functionality."""
        text = "This is a sample text that will be split into chunks. " * 5  # Make it longer than 100 chars
        chunks = self.chunker.chunk_text(text, source_url="http://example.com", title="Test Page")

        # Should have multiple chunks since the text is longer than chunk_size
        self.assertGreater(len(chunks), 1)

        # Each chunk should have content
        for chunk in chunks:
            self.assertIsInstance(chunk, DocumentationChunk)
            self.assertIsNotNone(chunk.content)
            self.assertLessEqual(len(chunk.content), 100)  # Should respect chunk size

    def test_chunk_text_short(self):
        """Test chunking of short text."""
        text = "Short text"
        chunks = self.chunker.chunk_text(text, source_url="http://example.com", title="Test Page")

        # Should have exactly one chunk
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].content, text)

    def test_chunk_text_empty(self):
        """Test chunking of empty text."""
        text = ""
        chunks = self.chunker.chunk_text(text, source_url="http://example.com", title="Test Page")

        # Should have no chunks
        self.assertEqual(len(chunks), 0)

    def test_chunk_by_paragraph(self):
        """Test chunking by paragraphs."""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        chunks = self.chunker.chunk_by_paragraph(text, source_url="http://example.com", title="Test Page")

        # Should have chunks based on paragraphs
        self.assertGreater(len(chunks), 0)

        # Each chunk should have content
        for chunk in chunks:
            self.assertIsInstance(chunk, DocumentationChunk)
            self.assertIsNotNone(chunk.content)


if __name__ == '__main__':
    unittest.main()