from bs4 import BeautifulSoup
import re
from typing import Dict, List


class HTMLCleaner:
    """
    A cleaner specifically designed for extracting clean text content from Docusaurus pages.
    """

    def __init__(self):
        # Define selectors for elements that should be removed
        self.selectors_to_remove = [
            'nav',  # Navigation elements
            '.navbar',  # Navigation bars
            '.nav',  # Navigation elements
            '.sidebar',  # Sidebar navigation
            '.theme-doc-sidebar',  # Docusaurus-specific sidebar
            '.menu',  # Menu elements
            '.footer',  # Footer
            '.pagination-nav',  # Pagination navigation
            '.theme-edit-this-page',  # Edit this page links
            '.theme-last-updated',  # Last updated info
            '.table-of-contents',  # Table of contents
            '.theme-admonition',  # Admonition blocks (notes, warnings, etc.)
            'script',  # Script tags
            'style',  # Style tags
            'noscript',  # Noscript tags
            '.code-block',  # Code blocks (may want to reconsider this)
            'header',  # Header elements (if not part of content)
            'footer',  # Footer elements
        ]

    def clean_docusaurus_page(self, html: str) -> str:
        """
        Clean HTML content from a Docusaurus page, extracting only the main content.

        Args:
            html: Raw HTML content from a Docusaurus page

        Returns:
            Clean text content with navigation and UI elements removed
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        for selector in self.selectors_to_remove:
            for element in soup.select(selector):
                element.decompose()

        # Look for the main content area - common Docusaurus selectors
        content_selectors = [
            '.main-wrapper',  # Common wrapper
            '.container',  # Container
            '.theme-doc-markdown',  # Docusaurus markdown content
            '.markdown',  # Markdown content
            '.doc-wrapper',  # Documentation wrapper
            '.theme-doc-page',  # Documentation page
            '.doc-page',  # Documentation page
            'main',  # Main content area
            '.content',  # Content area
            '.doc-content',  # Documentation content
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        # If we couldn't find a specific content area, use the body
        if not content_element:
            content_element = soup.find('body') or soup

        # Extract text from the content area
        text = content_element.get_text(separator=' ', strip=True)

        # Clean up the text
        text = self._clean_text(text)

        return text

    def _clean_text(self, text: str) -> str:
        """
        Clean up extracted text by removing extra whitespace and formatting issues.

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters that might have been extracted
        # Keep letters, numbers, punctuation, and common symbols
        text = re.sub(r'[^\w\s\-\.\,\!\?\;\:\(\)\[\]\{\}\'\"\/\@\#\$\%\&\*\+\=\|\<\>]+', ' ', text)

        # Remove extra spaces created by the previous operation
        text = re.sub(r'\s+', ' ', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def extract_page_title(self, html: str) -> str:
        """
        Extract the title from the HTML page.

        Args:
            html: Raw HTML content

        Returns:
            Page title, or an empty string if not found
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Try different methods to get the title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()

        # Look for h1 in the content area
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()

        # Look for meta tag with title
        meta_title = soup.find('meta', attrs={'property': 'og:title'})
        if meta_title:
            return meta_title.get('content', '').strip()

        return ""