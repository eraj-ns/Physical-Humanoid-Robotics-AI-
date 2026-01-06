import unittest
from src.utils import is_valid_url, sanitize_url, normalize_url


class TestUtils(unittest.TestCase):
    """
    Unit tests for utility functions.
    """

    def test_is_valid_url(self):
        """Test URL validation function."""
        # Valid URLs
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url("http://example.com"))
        self.assertTrue(is_valid_url("https://subdomain.example.com/path"))

        # Invalid URLs
        self.assertFalse(is_valid_url(""))
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url("ftp://example.com"))  # Assuming we only want http/https
        self.assertFalse(is_valid_url("just-a-string"))

    def test_sanitize_url(self):
        """Test URL sanitization function."""
        # Remove fragments
        self.assertEqual(sanitize_url("https://example.com/page#section"), "https://example.com/page")

        # Remove fragments with query params
        self.assertEqual(sanitize_url("https://example.com/page?param=value#section"), "https://example.com/page?param=value")

        # Handle whitespace
        self.assertEqual(sanitize_url("  https://example.com/page  "), "https://example.com/page")

    def test_normalize_url(self):
        """Test URL normalization function."""
        # Add https scheme if missing
        self.assertEqual(normalize_url("example.com"), "https://example.com")
        self.assertEqual(normalize_url("www.example.com"), "https://www.example.com")

        # Handle protocol-relative URLs
        self.assertEqual(normalize_url("//example.com"), "https://example.com")

        # Leave already complete URLs unchanged
        self.assertEqual(normalize_url("https://example.com"), "https://example.com")
        self.assertEqual(normalize_url("http://example.com"), "http://example.com")


if __name__ == '__main__':
    unittest.main()