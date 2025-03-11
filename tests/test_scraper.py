import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.scraper import fetch_url_content

def test_scraper():
    url = "https://www.bbc.com/news"
    content = fetch_url_content(url)
    assert content is not None, "Failed to fetch content"
    assert len(content) > 0, "Fetched content is empty"
    print("Test passed!")

if __name__ == "__main__":
    test_scraper()
