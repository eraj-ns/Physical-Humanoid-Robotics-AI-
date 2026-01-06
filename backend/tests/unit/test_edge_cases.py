import unittest
from unittest.mock import patch, MagicMock
from src.ingestion.crawler import DocusaurusCrawler
from src.ingestion.cleaner import HTMLCleaner
from src.ingestion.chunker import TextChunker
from src.config import Config
import requests


class TestEdgeCases(unittest.TestCase):
    """
    Test suite for edge cases and error conditions.
    """

    def test_crawler_empty_response(self):
        """Test crawler behavior with empty response."""
        crawler = DocusaurusCrawler()

        # Mock a response that returns empty content
        with patch.object(crawler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.text = ""
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            content = crawler.get_page_content("https://example.com")
            self.assertEqual(content, "")

    def test_crawler_http_error(self):
        """Test crawler behavior with HTTP errors."""
        crawler = DocusaurusCrawler()

        # Mock a response that raises an HTTP error
        with patch.object(crawler.session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")

            content = crawler.get_page_content("https://example.com")
            self.assertEqual(content, "")

    def test_crawler_connection_error(self):
        """Test crawler behavior with connection errors."""
        crawler = DocusaurusCrawler()

        # Mock a response that raises a connection error
        with patch.object(crawler.session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

            content = crawler.get_page_content("https://example.com")
            self.assertEqual(content, "")

    def test_crawler_timeout(self):
        """Test crawler behavior with timeout errors."""
        crawler = DocusaurusCrawler()

        # Mock a response that raises a timeout error
        with patch.object(crawler.session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

            content = crawler.get_page_content("https://example.com")
            self.assertEqual(content, "")

    def test_cleaner_empty_html(self):
        """Test cleaner behavior with empty HTML."""
        cleaner = HTMLCleaner()
        result = cleaner.clean_docusaurus_page("")
        self.assertEqual(result, "")

    def test_cleaner_malformed_html(self):
        """Test cleaner behavior with malformed HTML."""
        cleaner = HTMLCleaner()
        malformed_html = "<div><p>Unclosed paragraph"
        result = cleaner.clean_docusaurus_page(malformed_html)
        # Should not crash and return some text
        self.assertIsInstance(result, str)

    def test_cleaner_no_content(self):
        """Test cleaner behavior when no content is found."""
        cleaner = HTMLCleaner()
        html_with_only_nav = """
        <nav class="navbar">Navigation</nav>
        <footer>Footer</footer>
        """
        result = cleaner.clean_docusaurus_page(html_with_only_nav)
        # Should return empty or nearly empty string
        self.assertLess(len(result.strip()), 10)

    def test_chunker_empty_text(self):
        """Test chunker behavior with empty text."""
        chunker = TextChunker()
        result = chunker.chunk_text("", source_url="https://example.com", title="Test")
        self.assertEqual(len(result), 0)

    def test_chunker_single_char(self):
        """Test chunker behavior with single character."""
        chunker = TextChunker(chunk_size=10, chunk_overlap=0)
        result = chunker.chunk_text("a", source_url="https://example.com", title="Test")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].content, "a")

    def test_chunker_chunk_size_larger_than_text(self):
        """Test chunker when chunk size is larger than text."""
        chunker = TextChunker(chunk_size=1000, chunk_overlap=0)
        text = "Short text"
        result = chunker.chunk_text(text, source_url="https://example.com", title="Test")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].content, text)

    def test_config_validation_with_missing_values(self):
        """Test configuration validation with missing required values."""
        # Temporarily clear required config values
        original_key = Config.COHERE_API_KEY
        original_url = Config.QDRANT_URL

        try:
            Config.COHERE_API_KEY = ""
            Config.QDRANT_URL = ""

            errors = Config.validate()
            self.assertIn("COHERE_API_KEY is required", errors)
            self.assertIn("QDRANT_URL is required", errors)
        finally:
            # Restore original values
            Config.COHERE_API_KEY = original_key
            Config.QDRANT_URL = original_url

    def test_config_validation_invalid_values(self):
        """Test configuration validation with invalid values."""
        # Temporarily set invalid config values
        original_chunk_size = Config.CHUNK_SIZE
        original_chunk_overlap = Config.CHUNK_OVERLAP

        try:
            Config.CHUNK_SIZE = -1
            Config.CHUNK_OVERLAP = -5

            errors = Config.validate()
            self.assertIn("CHUNK_SIZE must be a positive integer", errors)
            self.assertIn("CHUNK_OVERLAP must be a non-negative integer", errors)
        finally:
            # Restore original values
            Config.CHUNK_SIZE = original_chunk_size
            Config.CHUNK_OVERLAP = original_chunk_overlap

    def test_config_validation_chunk_overlap_too_large(self):
        """Test configuration validation when chunk overlap is too large."""
        # Temporarily set invalid config values
        original_chunk_size = Config.CHUNK_SIZE
        original_chunk_overlap = Config.CHUNK_OVERLAP

        try:
            Config.CHUNK_SIZE = 100
            Config.CHUNK_OVERLAP = 150  # Larger than chunk size

            errors = Config.validate()
            self.assertIn("CHUNK_OVERLAP must be less than CHUNK_SIZE", errors)
        finally:
            # Restore original values
            Config.CHUNK_SIZE = original_chunk_size
            Config.CHUNK_OVERLAP = original_chunk_overlap


if __name__ == '__main__':
    unittest.main()