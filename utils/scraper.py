from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_url_content(url):
    try:
        with sync_playwright() as p:
            # Launch the browser
            browser = p.chromium.launch(headless=True)  # Set headless=False to see the browser in action
            page = browser.new_page()

            # Navigate to the page
            page.goto(url)

            # Wait for content to load (optional: adjust based on page structure)
            page.wait_for_selector('body')

            # Get the page content after rendering JavaScript
            html = page.content()

            # Use BeautifulSoup to parse the page
            soup = BeautifulSoup(html, 'html.parser')

            # Extract text from <p> and <div> tags
            paragraphs = soup.find_all(['p', 'div'])
            text = ' '.join([para.get_text() for para in paragraphs])

            browser.close()

            return text.strip()

    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None
