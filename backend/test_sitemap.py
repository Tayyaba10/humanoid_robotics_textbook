#!/usr/bin/env python3
"""
Test script to verify sitemap functionality for the humanoid robotics textbook
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sitemap_functionality():
    """Test the sitemap functionality to ensure all docs pages are discovered"""

    base_url = "https://tayyaba10.github.io/humanoid_robotics_textbook/"
    sitemap_url = urljoin(base_url, 'sitemap.xml')

    logger.info(f"Testing sitemap functionality for: {base_url}")
    logger.info(f"Sitemap URL: {sitemap_url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Test accessing the sitemap
        response = requests.get(sitemap_url, headers=headers, timeout=30)
        logger.info(f"Sitemap response status: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')

            # Check if it's a sitemap index
            if soup.find('sitemapindex'):
                logger.info("Found sitemap index, processing individual sitemaps")
                sitemap_locs = soup.find_all('loc')
                logger.info(f"Found {len(sitemap_locs)} individual sitemaps in index")

                # Process each individual sitemap
                total_urls = 0
                for sitemap_loc in sitemap_locs:
                    sitemap_loc_url = sitemap_loc.get_text().strip()
                    logger.info(f"Processing sitemap: {sitemap_loc_url}")

                    sitemap_response = requests.get(sitemap_loc_url, headers=headers, timeout=30)
                    if sitemap_response.status_code == 200:
                        sitemap_soup = BeautifulSoup(sitemap_response.content, 'xml')
                        urls = sitemap_soup.find_all('loc')
                        logger.info(f"Found {len(urls)} URLs in sitemap: {sitemap_loc_url}")

                        # Check for documentation pages
                        doc_urls = [url.get_text().strip() for url in urls if '/docs/' in url.get_text()]
                        logger.info(f"Found {len(doc_urls)} documentation URLs in this sitemap")

                        for doc_url in doc_urls[:5]:  # Show first 5 doc URLs
                            logger.info(f"  - {doc_url}")

                        total_urls += len(urls)

                logger.info(f"Total URLs found from sitemap index: {total_urls}")

            else:
                # Regular sitemap
                logger.info("Processing regular sitemap")
                urls = soup.find_all('loc')
                logger.info(f"Found {len(urls)} total URLs in sitemap")

                # Check for documentation pages
                doc_urls = [url.get_text().strip() for url in urls if '/docs/' in url.get_text()]
                logger.info(f"Found {len(doc_urls)} documentation URLs in sitemap")

                for doc_url in doc_urls[:10]:  # Show first 10 doc URLs
                    logger.info(f"  - {doc_url}")

        # Test if specific documentation page exists
        test_doc_url = "https://tayyaba10.github.io/humanoid_robotics_textbook/docs/ros2/chapter-1.1-introduction-to-ros2/"
        test_response = requests.get(test_doc_url, headers=headers, timeout=30)
        logger.info(f"Test doc page ({test_doc_url}) status: {test_response.status_code}")

        return True

    except Exception as e:
        logger.error(f"Error testing sitemap functionality: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing sitemap functionality...")
    success = test_sitemap_functionality()
    if success:
        logger.info("Sitemap test completed successfully!")
    else:
        logger.error("Sitemap test failed!")