import requests
from bs4 import BeautifulSoup
import re
import time
import random
import streamlit as st

def fetch_web_content(url, cache=True):
    """
    Fetch content from a web URL with caching to avoid repeated requests.
    """
    # Use Streamlit's caching mechanism if enabled
    if cache:
        return _cached_fetch_web_content(url)
    else:
        return _fetch_web_content(url)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def _cached_fetch_web_content(url):
    """Cached version of the web content fetcher"""
    return _fetch_web_content(url)

def _fetch_web_content(url):
    """Actual implementation of the web content fetcher"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Error fetching content from {url}: {str(e)}")
        return None

def extract_wikipedia_section(html_content, section_id=None):
    """
    Extract specific section from Wikipedia article.
    If section_id is None, extract the introduction.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    if section_id:
        # Find the section heading
        section_heading = soup.find(id=section_id)
        if not section_heading:
            return None
        
        # Get the parent element (usually a heading tag like h2, h3, etc.)
        parent = section_heading.parent
        
        # Extract all paragraphs until the next heading of same or higher level
        section_text = ""
        current = parent.find_next_sibling()
        while current and not (current.name and current.name[0] == 'h' and int(current.name[1]) <= int(parent.name[1])):
            if current.name == 'p':
                section_text += current.text + " "
            current = current.find_next_sibling()
        
        return section_text
    else:
        # Extract the introduction (paragraphs before the first heading)
        intro_text = ""
        first_heading = soup.find(['h1', 'h2'])
        
        if first_heading:
            current = soup.find('p')
            while current and current != first_heading:
                if current.name == 'p':
                    intro_text += current.text + " "
                current = current.find_next_sibling()
        else:
            # If no headings found, just get the first few paragraphs
            paragraphs = soup.find_all('p', limit=3)
            for p in paragraphs:
                intro_text += p.text + " "
        
        return intro_text

def search_youtube_videos(query, max_results=5):
    """
    Simple function to get YouTube video links based on a search query.
    Note: This doesn't use the YouTube API, just a basic search scrape.
    For a production application, consider using the YouTube API.
    """
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    
    html_content = fetch_web_content(search_url, cache=True)
    if not html_content:
        return []
    
    # Extract video IDs from the search results
    video_ids = re.findall(r"watch\?v=(\S{11})", html_content)
    
    # Remove duplicates while preserving order
    unique_ids = []
    for video_id in video_ids:
        if video_id not in unique_ids:
            unique_ids.append(video_id)
    
    # Create video URLs
    video_urls = [f"https://www.youtube.com/watch?v={vid}" for vid in unique_ids[:max_results]]
    
    return video_urls