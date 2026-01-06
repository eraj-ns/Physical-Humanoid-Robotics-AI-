import logging
import sys
from typing import Optional
from urllib.parse import urlparse
import re


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Set up logging with configurable levels.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               If None, uses INFO as default.

    Returns:
        Configured logger instance
    """
    if level is None:
        level = "INFO"

    # Convert string level to logging constant
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create a custom logger
    logger = logging.getLogger('book_embedding_ingestion')
    logger.setLevel(log_level)

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Create formatters and add it to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    return logger


def is_valid_url(url: str) -> bool:
    """
    Validate if the given string is a properly formatted URL.

    Args:
        url: URL string to validate

    Returns:
        True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_url(url: str) -> str:
    """
    Sanitize a URL by removing fragments and normalizing it.

    Args:
        url: URL string to sanitize

    Returns:
        Sanitized URL string
    """
    # Remove fragments (part after #)
    if '#' in url:
        url = url.split('#')[0]

    # Remove query parameters if they're not needed (optional, can be removed for some use cases)
    # For documentation sites, we might want to keep query params, so we'll just normalize the URL
    return url.strip()


def normalize_url(url: str) -> str:
    """
    Normalize a URL by ensuring it has proper formatting.

    Args:
        url: URL string to normalize

    Returns:
        Normalized URL string
    """
    # Ensure the URL has a scheme
    if not url.startswith(('http://', 'https://')):
        if url.startswith('//'):
            url = 'https:' + url
        else:
            url = 'https://' + url

    return url


def generate_content_checksum(content: str) -> str:
    """
    Generate a checksum for content to detect changes.

    Args:
        content: Content string to generate checksum for

    Returns:
        Hexadecimal checksum string
    """
    import hashlib
    # Use SHA-256 to generate a hash of the content
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return content_hash