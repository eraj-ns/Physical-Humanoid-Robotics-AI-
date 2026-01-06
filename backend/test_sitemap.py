"""
Test script to verify sitemap.xml functionality
"""
from src.ingestion.crawler import DocusaurusCrawler

def test_sitemap_crawling():
    """Test the sitemap crawling functionality with the provided URL"""
    crawler = DocusaurusCrawler(max_pages=100, delay=0.5)  # Allow more pages and shorter delay for testing

    # Test with the URL provided by the user
    test_url = "https://physical-humanoid-robotics-ai-ym52.vercel.app/"

    print(f"Testing sitemap crawling for: {test_url}")

    # First, try to get URLs from sitemap
    sitemap_urls = crawler.get_sitemap_urls(test_url)

    print(f"Found {len(sitemap_urls)} URLs in sitemap:")
    for i, url in enumerate(sitemap_urls[:10]):  # Print first 10 URLs
        print(f"  {i+1}. {url}")

    if len(sitemap_urls) > 10:
        print(f"  ... and {len(sitemap_urls) - 10} more URLs")

    # Now try crawling the site
    print(f"\nStarting crawl of {test_url}")
    crawled_urls = crawler.crawl_site(test_url)

    print(f"Crawled {len(crawled_urls)} pages:")
    for i, url in enumerate(crawled_urls):
        print(f"  {i+1}. {url}")

if __name__ == "__main__":
    test_sitemap_crawling()