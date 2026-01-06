import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.ingestion.main import main_ingestion_function
from src.ingestion.crawler import DocusaurusCrawler
from src.ingestion.cleaner import HTMLCleaner
from src.ingestion.chunker import TextChunker


class TestIngestionPipelineIntegration(unittest.TestCase):
    """
    Integration tests for the ingestion pipeline components.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Sample HTML content for testing
        self.sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Documentation</title>
        </head>
        <body>
            <nav class="navbar">Navigation content to be ignored</nav>
            <div class="main-wrapper">
                <div class="doc-page">
                    <h1>Test Documentation Page</h1>
                    <p>This is the main content of the documentation page.</p>
                    <p>It contains multiple paragraphs that should be extracted.</p>
                    <h2>Section 1</h2>
                    <p>Content for section 1.</p>
                    <h2>Section 2</h2>
                    <p>Content for section 2.</p>
                </div>
            </div>
            <footer>Footer content to be ignored</footer>
        </body>
        </html>
        """

    @patch.object(DocusaurusCrawler, 'get_page_content')
    @patch.object(DocusaurusCrawler, 'crawl_site')
    def test_ingestion_pipeline_integration(self, mock_crawl_site, mock_get_content):
        """Test the integration of crawler, cleaner, and chunker components."""
        # Mock the crawler to return our test URL
        mock_crawl_site.return_value = ["https://example.com/test-page"]
        mock_get_content.return_value = self.sample_html

        # Run the main ingestion function with a test URL
        result = main_ingestion_function(urls=["https://example.com"])

        # Verify that we got chunks back
        self.assertGreater(len(result), 0)

        # Verify that the chunks have content
        for chunk in result:
            self.assertIsNotNone(chunk.content)
            self.assertNotEqual(chunk.content.strip(), "")
            self.assertEqual(chunk.source_url, "https://example.com/test-page")

    def test_crawler_cleaner_integration(self):
        """Test the integration between crawler and cleaner components."""
        cleaner = HTMLCleaner()

        # Test cleaning the sample HTML
        clean_content = cleaner.clean_docusaurus_page(self.sample_html)

        # Verify that navigation and footer content were removed
        self.assertNotIn("Navigation content to be ignored", clean_content)
        self.assertNotIn("Footer content to be ignored", clean_content)

        # Verify that main content was preserved
        self.assertIn("main content of the documentation page", clean_content)
        self.assertIn("multiple paragraphs that should be extracted", clean_content)

        # Verify that the content is properly cleaned (no HTML tags)
        self.assertNotIn("<p>", clean_content.lower())
        self.assertNotIn("<h1>", clean_content.lower())
        self.assertNotIn("</div>", clean_content.lower())

    def test_cleaner_chunker_integration(self):
        """Test the integration between cleaner and chunker components."""
        cleaner = HTMLCleaner()
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)

        # Clean the sample HTML
        clean_content = cleaner.clean_docusaurus_page(self.sample_html)

        # Verify we got clean text
        self.assertGreater(len(clean_content), 0)

        # Chunk the clean content
        chunks = chunker.chunk_text(clean_content, source_url="https://example.com/test", title="Test Page")

        # Verify we got chunks
        self.assertGreater(len(chunks), 0)

        # Verify each chunk has content
        for chunk in chunks:
            self.assertIsNotNone(chunk.content)
            self.assertLessEqual(len(chunk.content), 100)  # Should respect chunk size


if __name__ == '__main__':
    unittest.main()