import argparse
from ..config import validate_environment, Config
from ..utils import setup_logging
from .crawler import DocusaurusCrawler
from .cleaner import HTMLCleaner
from .chunker import TextChunker
from ..models.data_models import DocumentationChunk
from typing import List
import sys


def main_ingestion_function(urls: List[str] = None) -> List[DocumentationChunk]:
    """
    Main ingestion function that runs the full pipeline:
    1. Crawls Docusaurus URLs
    2. Extracts clean text content
    3. Chunks the text into segments

    Args:
        urls: List of URLs to crawl. If None, uses URLs from configuration.

    Returns:
        List of DocumentationChunk objects containing the processed content
    """
    logger = setup_logging(Config.LOG_LEVEL)

    # Validate environment configuration
    if not validate_environment():
        logger.error("Environment configuration validation failed")
        sys.exit(1)

    # Use provided URLs or get from config
    if not urls:
        urls = Config.DOCUMENTATION_URLS

    if not urls or urls == [""]:
        logger.error("No documentation URLs provided")
        sys.exit(1)

    all_chunks = []
    total_urls = len(urls)

    for idx, url in enumerate(urls, 1):
        logger.info(f"Processing documentation site {idx}/{total_urls}: {url}")

        # Initialize components
        crawler = DocusaurusCrawler(max_pages=50, delay=1.0)  # Reasonable limits for demo
        cleaner = HTMLCleaner()
        chunker = TextChunker(chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP)

        # Crawl the site
        logger.info(f"Starting crawl for {url}")
        site_urls = crawler.crawl_site(url)
        logger.info(f"Crawled {len(site_urls)} pages from {url}")

        # Process each page
        total_pages = len(site_urls)
        for page_idx, page_url in enumerate(site_urls, 1):
            logger.info(f"Processing page {page_idx}/{total_pages}: {page_url}")

            # Get page content
            html_content = crawler.get_page_content(page_url)
            if not html_content:
                logger.warning(f"Could not retrieve content for {page_url}")
                continue

            # Extract page title
            title = cleaner.extract_page_title(html_content)

            # Clean the HTML to extract text content
            clean_text = cleaner.clean_docusaurus_page(html_content)

            if not clean_text.strip():
                logger.warning(f"No content extracted from {page_url}")
                continue

            # Chunk the text
            chunks = chunker.chunk_by_paragraph(clean_text, source_url=page_url, title=title)

            # Add to all chunks
            all_chunks.extend(chunks)

            logger.info(f"Extracted {len(chunks)} chunks from {page_url}")

        logger.info(f"Completed processing for {url}")

    logger.info(f"Ingestion completed. Total chunks: {len(all_chunks)}")
    return all_chunks


def run_full_pipeline(urls: List[str] = None, store_embeddings: bool = False):
    """
    Run the full pipeline including ingestion, embedding generation, and storage.

    Args:
        urls: List of URLs to process. If None, uses URLs from configuration.
        store_embeddings: Whether to generate embeddings and store them in Qdrant
    """
    logger = setup_logging(Config.LOG_LEVEL)

    try:
        logger.info("Starting full documentation pipeline")

        # Step 1: Ingest content
        logger.info("Step 1: Ingesting documentation content...")
        chunks = main_ingestion_function(urls)
        logger.info(f"Step 1 completed. Generated {len(chunks)} content chunks")

        if store_embeddings:
            # Step 2: Generate embeddings
            logger.info("Step 2: Generating embeddings...")
            try:
                from ..embeddings.generator import CohereEmbeddingService
                logger.info("Initializing Cohere embedding service...")
                embedding_service = CohereEmbeddingService()
                logger.info("Starting embedding generation for chunks...")
                embeddings = embedding_service.generate_embedding_for_chunks(chunks)
                logger.info(f"Step 2 completed. Generated {len(embeddings)} embeddings")
            except Exception as e:
                logger.error(f"Step 2 failed: {str(e)}")
                raise

            # Step 3: Store embeddings in Qdrant
            logger.info("Step 3: Storing embeddings in Qdrant...")
            try:
                from ..storage.qdrant_client import QdrantStorage
                logger.info("Initializing Qdrant storage client...")
                qdrant_client = QdrantStorage()

                logger.info("Creating/validating Qdrant collection...")
                # Create collection if it doesn't exist
                qdrant_client.create_collection()

                logger.info(f"Storing {len(embeddings)} embeddings in Qdrant...")
                # Store embeddings
                success = qdrant_client.store_embeddings(embeddings)
                if success:
                    logger.info("Step 3 completed. Embeddings stored successfully")
                else:
                    logger.error("Step 3 failed. Could not store embeddings")
                    raise Exception("Failed to store embeddings in Qdrant")
            except Exception as e:
                logger.error(f"Step 3 failed: {str(e)}")
                raise

        logger.info("Full pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        sys.exit(1)


def main():
    """
    Main function to run the ingestion pipeline from command line.
    """
    parser = argparse.ArgumentParser(description="Book Embedding Ingestion Pipeline")
    parser.add_argument("--urls", nargs="+", help="List of URLs to process (overrides config)")
    parser.add_argument("--store", action="store_true", help="Generate embeddings and store in Qdrant")
    parser.add_argument("--config", help="Path to config file (not implemented in this version)")

    args = parser.parse_args()

    logger = setup_logging(Config.LOG_LEVEL)
    logger.info("Starting documentation ingestion pipeline")

    # Run the full pipeline
    run_full_pipeline(urls=args.urls, store_embeddings=args.store)


if __name__ == "__main__":
    main()