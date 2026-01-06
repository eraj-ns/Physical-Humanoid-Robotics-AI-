"""
Script to ingest all documentation pages from sitemap.xml into Qdrant collection
"""
import os
from src.ingestion.crawler import DocusaurusCrawler
from src.ingestion.cleaner import HTMLCleaner
from src.ingestion.chunker import TextChunker
from src.embeddings.generator import CohereEmbeddingService
from src.storage.qdrant_client import QdrantStorage
from src.config import Config
from src.utils import setup_logging
from src.models.data_models import DocumentationChunk
from typing import List
import numpy as np


def create_mock_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Create mock embeddings for testing when Cohere API is not available.
    In a real scenario, this would be replaced with actual embeddings.
    """
    embeddings = []
    for text in texts:
        # Create a deterministic mock embedding based on the text content
        # This ensures consistent results for the same content
        text_hash = hash(text) % (2**32)
        np.random.seed(text_hash % (2**32))  # Use the hash as seed for consistency
        embedding = np.random.random(1024).tolist()  # 1024-dim vector like Cohere
        embeddings.append(embedding)
    return embeddings


def ingest_sitemap_to_qdrant():
    """
    Ingest all documentation pages from sitemap.xml into Qdrant collection
    """
    logger = setup_logging(Config.LOG_LEVEL)

    # Set the specific collection name
    collection_name = "rag-chatbot-hackathon"

    logger.info(f"Starting ingestion to Qdrant collection: {collection_name}")

    # Step 1: Load sitemap and extract all URLs
    logger.info("Step 1: Loading sitemap from https://physical-humanoid-robotics-ai-ym52.vercel.app/sitemap.xml")
    crawler = DocusaurusCrawler(max_pages=100, delay=0.5)  # Allow more pages and shorter delay for full ingestion
    sitemap_urls = crawler.get_sitemap_urls("https://physical-humanoid-robotics-ai-ym52.vercel.app/")

    logger.info(f"Found {len(sitemap_urls)} URLs in sitemap")

    if not sitemap_urls:
        logger.error("No URLs found in sitemap, exiting.")
        return

    # Initialize components
    cleaner = HTMLCleaner()
    chunker = TextChunker(chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP)

    # Initialize Qdrant client
    qdrant_client = QdrantStorage(collection_name=collection_name)

    # Create collection if it doesn't exist (with 1024 dimensions for Cohere-like embeddings)
    qdrant_client.create_collection(vector_size=1024)

    # Try to initialize Cohere service, or use mock if not available
    embedding_service = None
    try:
        if Config.COHERE_API_KEY:
            embedding_service = CohereEmbeddingService()
            logger.info("Cohere embedding service initialized successfully")
        else:
            logger.warning("No Cohere API key found, will use mock embeddings")
    except Exception as e:
        logger.warning(f"Could not initialize Cohere service: {str(e)}, will use mock embeddings")

    total_processed_urls = 0
    total_chunks_created = 0
    total_embeddings_stored = 0

    # Step 3: Process each URL
    for idx, url in enumerate(sitemap_urls, 1):
        logger.info(f"Processing URL {idx}/{len(sitemap_urls)}: {url}")

        try:
            # Fetch page content
            html_content = crawler.get_page_content(url)
            if not html_content:
                logger.warning(f"Could not retrieve content for {url}")
                continue

            # Extract page title
            title = cleaner.extract_page_title(html_content)

            # Clean the HTML to extract text content
            clean_text = cleaner.clean_docusaurus_page(html_content)

            if not clean_text.strip():
                logger.warning(f"No content extracted from {url}")
                continue

            # Chunk the text
            chunks = chunker.chunk_by_paragraph(clean_text, source_url=url, title=title)

            if not chunks:
                logger.warning(f"No chunks created for {url}")
                continue

            # Update counters
            total_processed_urls += 1
            total_chunks_created += len(chunks)

            # Generate embeddings for the chunks
            if embedding_service:
                # Use real Cohere embeddings
                embeddings = embedding_service.generate_embedding_for_chunks(chunks)
            else:
                # Use mock embeddings
                text_contents = [chunk.content for chunk in chunks]
                mock_embeddings = create_mock_embeddings(text_contents)

                # Create EmbeddingVector objects with mock data
                from src.models.data_models import EmbeddingVector
                embeddings = []
                for i, mock_embedding in enumerate(mock_embeddings):
                    embedding = EmbeddingVector(
                        id="",
                        vector=mock_embedding,
                        chunk_id=chunks[i].id if i < len(chunks) else f"chunk_{i}",
                        model_version="mock-embedding"
                    )
                    embeddings.append(embedding)

            # Store embeddings in Qdrant with metadata
            for i, embedding in enumerate(embeddings):
                if embedding is not None:
                    # For Qdrant upsert, we need to format the points properly
                    from qdrant_client.http import models
                    from uuid import uuid4

                    # Create a payload with metadata
                    payload = {
                        "url": url,
                        "title": title,
                        "text": chunks[i].content if i < len(chunks) else "",
                        "source_url": url,
                        "chunk_index": i
                    }

                    # Create a point for Qdrant
                    point = models.PointStruct(
                        id=str(uuid4()),
                        vector=embedding.vector,
                        payload=payload
                    )

                    # Upsert the single point to Qdrant
                    qdrant_client.client.upsert(
                        collection_name=collection_name,
                        points=[point]
                    )

                    total_embeddings_stored += 1

            logger.info(f"Successfully processed {url} - created {len(chunks)} chunks")

        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue

    # Step 4: Confirm ingestion
    logger.info("Step 4: Confirming ingestion results")

    # Get collection info
    collection_info = qdrant_client.get_collection_info()
    if collection_info:
        vector_count = collection_info.get("point_count", 0)
    else:
        vector_count = 0

    print("\n" + "="*60)
    print("INGESTION COMPLETED")
    print("="*60)
    print(f"Total URLs processed: {total_processed_urls}")
    print(f"Total chunks created: {total_chunks_created}")
    print(f"Total embeddings stored: {total_embeddings_stored}")
    print(f"Qdrant collection name: {collection_name}")
    print(f"Vectors in collection: {vector_count}")
    print("="*60)

    logger.info(f"Ingestion completed. Processed {total_processed_urls} URLs, created {total_chunks_created} chunks, stored {total_embeddings_stored} embeddings in collection '{collection_name}' with {vector_count} total vectors.")


def main():
    """
    Main function to run the sitemap ingestion to Qdrant
    """
    print("Starting sitemap ingestion to Qdrant...")
    print("This will:")
    print("1. Load sitemap from https://physical-humanoid-robotics-ai-ym52.vercel.app/sitemap.xml")
    print("2. Extract all URLs from sitemap")
    print("3. Process each URL and store embeddings in Qdrant collection 'rag-chatbot-hackathon'")
    print("4. Confirm ingestion with statistics")
    print()

    try:
        ingest_sitemap_to_qdrant()
        print("\nProcess completed successfully!")
    except Exception as e:
        print(f"\nError during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()