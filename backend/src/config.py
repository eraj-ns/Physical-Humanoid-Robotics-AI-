import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class to manage all environment variables and settings
    for the book embedding ingestion pipeline.
    """

    # Cohere Configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "docs_embeddings")

    # Documentation URLs
    DOCUMENTATION_URLS: List[str] = os.getenv("DOCUMENTATION_URLS", "").split(",") if os.getenv("DOCUMENTATION_URLS") else []

    # Text Processing Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> List[str]:
        """
        Validate configuration values and return a list of validation errors.

        Returns:
            List of validation error messages. Empty list if all validations pass.
        """
        errors = []

        if not cls.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is required")

        if not cls.QDRANT_URL:
            errors.append("QDRANT_URL is required")

        if not cls.DOCUMENTATION_URLS or cls.DOCUMENTATION_URLS == [""]:
            errors.append("At least one DOCUMENTATION_URLS is required")

        if cls.CHUNK_SIZE <= 0:
            errors.append("CHUNK_SIZE must be a positive integer")

        if cls.CHUNK_OVERLAP < 0:
            errors.append("CHUNK_OVERLAP must be a non-negative integer")

        if cls.CHUNK_OVERLAP >= cls.CHUNK_SIZE:
            errors.append("CHUNK_OVERLAP must be less than CHUNK_SIZE")

        return errors


def validate_environment() -> bool:
    """
    Validate the environment configuration and print errors if any.

    Returns:
        True if all validations pass, False otherwise.
    """
    errors = Config.validate()

    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


def get_config_value(key: str, default: str = "") -> str:
    """
    Get a configuration value with a default fallback.

    Args:
        key: The environment variable key to retrieve
        default: The default value if the key is not found

    Returns:
        The value of the environment variable or the default value
    """
    return os.getenv(key, default)