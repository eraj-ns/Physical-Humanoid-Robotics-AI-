import requests
from bs4 import BeautifulSoup
from typing import List, Set
from urllib.parse import urljoin, urlparse
import time
import logging
from ..utils import setup_logging
import random
import xml.etree.ElementTree as ET

logger = setup_logging()


class DocusaurusCrawler:
    """
    A crawler specifically designed for Docusaurus-based documentation sites.
    """

    def __init__(self, max_pages: int = 100, delay: float = 1.0):
        """
        Initialize the Docusaurus crawler.

        Args:
            max_pages: Maximum number of pages to crawl
            delay: Delay in seconds between requests to be respectful to the server
        """
        self.max_pages = max_pages
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BookEmbeddingBot/1.0)'
        })

    def get_page_content(self, url: str, max_retries: int = 3) -> str:
        """
        Fetch and return the content of a single page with retry logic.

        Args:
            url: The URL to fetch content from
            max_retries: Maximum number of retry attempts

        Returns:
            The HTML content of the page, or empty string if all retries fail
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    logger.warning(f"Page not found (404) at {url}")
                    return ""  # Don't retry 404 errors
                elif response.status_code == 403:
                    logger.warning(f"Access forbidden (403) at {url}")
                    return ""  # Don't retry 403 errors
                else:
                    logger.warning(f"HTTP error {response.status_code} at {url} (attempt {attempt + 1}/{max_retries})")
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                        return ""
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error at {url} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                    return ""
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout error at {url} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                    return ""
            except requests.RequestException as e:
                logger.warning(f"Request error at {url} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                    return ""

            # Exponential backoff with jitter: wait 1s, 2s, 4s + random jitter
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)

        return ""

    def extract_links(self, html: str, base_url: str) -> Set[str]:
        """
        Extract all valid links from the HTML content.

        Args:
            html: HTML content to extract links from
            base_url: Base URL to resolve relative links

        Returns:
            Set of valid URLs found on the page
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Only include links that are on the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                # Filter out non-HTML links and anchor links
                if full_url.endswith(('.html', '/')) and not full_url.startswith('#'):
                    links.add(full_url)

        return links

    def is_valid_docusaurus_page(self, html: str) -> bool:
        """
        Check if the page appears to be a valid Docusaurus page.

        Args:
            html: HTML content to check

        Returns:
            True if the page appears to be a valid Docusaurus page
        """
        # Look for common Docusaurus indicators
        soup = BeautifulSoup(html, 'html.parser')

        # Check for Docusaurus-specific classes or elements
        docusaurus_indicators = [
            'navbar',
            'main-wrapper',
            'doc-page',
            'container',
            'theme-doc-sidebar',
            'doc-wrapper'
        ]

        for indicator in docusaurus_indicators:
            if soup.find(class_=indicator) or soup.find(id=indicator):
                return True

        # Check for common Docusaurus script tags
        scripts = soup.find_all('script')
        for script in scripts:
            if script.get('src') and 'docusaurus' in (script.get('src') or ''):
                return True

        return False

    def get_sitemap_urls(self, base_url: str) -> List[str]:
        """
        Extract URLs from the sitemap.xml file of the given base URL.

        Args:
            base_url: Base URL of the website to get sitemap from

        Returns:
            List of URLs extracted from the sitemap
        """
        sitemap_urls = []

        # Try different common sitemap locations
        sitemap_locations = [
            urljoin(base_url, 'sitemap.xml'),
            urljoin(base_url, 'sitemap_index.xml'),
            urljoin(base_url, 'sitemap/sitemap.xml'),
            base_url.rstrip('/') + '/sitemap.xml'
        ]

        for sitemap_url in sitemap_locations:
            try:
                logger.info(f"Trying to fetch sitemap from: {sitemap_url}")
                response = self.session.get(sitemap_url, timeout=10)

                if response.status_code == 200:
                    logger.info(f"Successfully fetched sitemap from: {sitemap_url}")

                    # Parse the sitemap XML
                    try:
                        root = ET.fromstring(response.content)

                        # Handle regular sitemap
                        if 'urlset' in root.tag:
                            for url_element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                                sitemap_urls.append(url_element.text.strip())
                            # Also try without namespace
                            for url_element in root.findall('.//loc'):
                                if not url_element.text.startswith('http://www.sitemaps.org'):
                                    sitemap_urls.append(url_element.text.strip())

                        # Handle sitemap index (sitemap of sitemaps)
                        elif 'sitemapindex' in root.tag:
                            sitemap_locations = []
                            for sitemap_element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                                sitemap_locations.append(sitemap_element.text.strip())
                            # Also try without namespace
                            for sitemap_element in root.findall('.//loc'):
                                if not sitemap_element.text.startswith('http://www.sitemaps.org'):
                                    sitemap_locations.append(sitemap_element.text.strip())

                            # Fetch each individual sitemap
                            for sub_sitemap_url in sitemap_locations:
                                try:
                                    sub_response = self.session.get(sub_sitemap_url, timeout=10)
                                    if sub_response.status_code == 200:
                                        sub_root = ET.fromstring(sub_response.content)
                                        for url_element in sub_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                                            sitemap_urls.append(url_element.text.strip())
                                        # Also try without namespace
                                        for url_element in sub_root.findall('.//loc'):
                                            if not url_element.text.startswith('http://www.sitemaps.org'):
                                                sitemap_urls.append(url_element.text.strip())
                                except ET.ParseError:
                                    logger.warning(f"Could not parse sitemap: {sub_sitemap_url}")
                                except requests.RequestException as e:
                                    logger.warning(f"Error fetching sitemap {sub_sitemap_url}: {str(e)}")

                        logger.info(f"Found {len(sitemap_urls)} URLs in sitemap")
                        break  # If we successfully got URLs from one sitemap, we can stop
                    except ET.ParseError:
                        logger.warning(f"Could not parse sitemap XML from: {sitemap_url}")
                        continue
                else:
                    logger.info(f"Sitemap not found at: {sitemap_url} (status: {response.status_code})")
            except requests.RequestException as e:
                logger.warning(f"Error fetching sitemap from {sitemap_url}: {str(e)}")
                continue

        return list(set(sitemap_urls))  # Remove duplicates

    def crawl_site(self, start_url: str) -> List[str]:
        """
        Crawl a Docusaurus site starting from the given URL.
        First tries to get URLs from sitemap.xml for comprehensive coverage.

        Args:
            start_url: The starting URL for the crawl

        Returns:
            List of URLs found during the crawl
        """
        visited_urls = set()
        all_urls = []

        logger.info(f"Starting crawl of {start_url}")
        logger.info(f"Max pages to crawl: {self.max_pages}")

        # First, try to get URLs from sitemap.xml for comprehensive coverage
        logger.info("Attempting to retrieve URLs from sitemap.xml...")
        sitemap_urls = self.get_sitemap_urls(start_url)

        if sitemap_urls:
            logger.info(f"Found {len(sitemap_urls)} URLs from sitemap, using these for crawling")
            urls_to_visit = sitemap_urls
        else:
            logger.info("No sitemap found, using traditional crawling approach")
            urls_to_visit = [start_url]

        # Process URLs from sitemap or traditional crawling
        for url in urls_to_visit:
            if len(visited_urls) >= self.max_pages:
                break

            if url in visited_urls:
                continue

            logger.info(f"Crawling ({len(visited_urls) + 1}/{min(self.max_pages, len(urls_to_visit))}): {url}")
            visited_urls.add(url)

            html_content = self.get_page_content(url)
            if not html_content:
                logger.warning(f"Failed to retrieve content for {url}")
                continue

            # Check if this looks like a Docusaurus page
            if not self.is_valid_docusaurus_page(html_content):
                logger.warning(f"Skipping non-Docusaurus page: {url}")
                continue

            all_urls.append(url)

            # Be respectful to the server
            time.sleep(self.delay)

        logger.info(f"Crawl completed. Visited {len(visited_urls)} pages, found {len(all_urls)} valid Docusaurus pages.")
        return all_urls