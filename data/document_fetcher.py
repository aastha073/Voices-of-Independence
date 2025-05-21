"""
Functions for fetching documents from various sources.
"""

import requests
from bs4 import BeautifulSoup
import re
import logging
from utils.opik_tracking import opik

logger = logging.getLogger(__name__)

@opik.track
def fetch_document(doc_info):
    """Fetch and extract text from a URL.
    
    Args:
        doc_info (dict): Document information including URL and title
        
    Returns:
        str: The extracted text content
    """
    url = doc_info["url"]
    logger.info(f"Fetching {doc_info['title']} from {url}")
    
    try:
        response = requests.get(url, timeout=30)
        if not response.ok:
            logger.error(f"Failed to fetch {url}: {response.status_code}")
            return None
        
        content = response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return None
    
    # Process different content types
    return _process_content(content, url)

def _process_content(content, url):
    """Process different content types based on the URL."""
    # For plain text files
    if url.endswith('.txt'):
        return content
    
    # For Project Gutenberg texts
    if 'gutenberg.org' in url:
        # Extract the main content from Project Gutenberg texts
        match = re.search(r'\*\*\*\s+START OF.*?\*\*\*(.+?)\*\*\*\s+END OF', content, re.DOTALL)
        text = match.group(1) if match else content
        return _clean_text(text)
    
    # For HTML content
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    
    # Special case for archives.gov
    if 'archives.gov' in url:
        main_content = soup.find('div', class_='main-content')
        if main_content:
            return _clean_text(main_content.get_text())
    
    # Special case for founders.archives.gov
    if 'founders.archives.gov' in url:
        doc_content = soup.find('div', class_='doc-content')
        if doc_content:
            return _clean_text(doc_content.get_text())
    
    # Special case for avalon.law.yale.edu
    if 'avalon.law.yale.edu' in url:
        body = soup.find('body')
        if body:
            return _clean_text(body.get_text())
    
    # Default: extract all text
    return _clean_text(soup.get_text())

def _clean_text(text):
    """Clean up the extracted text."""
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common headers/footers from sources
    text = re.sub(r'Note: The following text is a transcription.*?original text\.', '', text, flags=re.DOTALL)
    
    return text