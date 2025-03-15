from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import Document

def fetch_url_content(url):
    try:
        loader = WebBaseLoader(url)  # Initialize the WebBaseLoader with the URL
        documents = loader.load()  # Load documents from the URL

        if documents:
            text = " ".join([doc.page_content for doc in documents])
            return text.strip()
        else:
            print("No content fetched from the URL.")
            return None
    except Exception as e:
        print(f"Error fetching URL content: {e}")
        return None
