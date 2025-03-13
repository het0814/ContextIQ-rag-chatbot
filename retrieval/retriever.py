from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import os

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Create or load the Chroma vector store
DB_PATH = "embeddings/chroma"
vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

def add_document(text, metadata=None):
    try:
        doc = Document(page_content=text, metadata=metadata or {})
        vector_store.add_documents([doc])
        vector_store.persist()
        print("Document added to vector store.")
    except Exception as e:
        print(f"Error adding document: {e}")

def retrieve_context(query, top_k=3):
    try:
        results = vector_store.similarity_search(query, k=top_k)
        return [result.page_content for result in results]
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return []
