import requests
from bs4 import BeautifulSoup
def fetch_url_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from <p> and <div> tags
        paragraphs = soup.find_all(['p', 'div'])
        text = ' '.join([para.get_text() for para in paragraphs])

        return text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
