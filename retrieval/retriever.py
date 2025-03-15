from langchain_community.vectorstores import Chroma 
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.2,openai_api_key=OPENAI_API_KEY)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Create or load the Chroma vector store
DB_PATH = "embeddings/chroma"
vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

# Initialize conversation memory (stores previous queries + answers)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Create the conversational chain using retriever + memory
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

def add_document(text, metadata=None):
    try:
        doc = Document(page_content=text, metadata=metadata or {})
        vector_store.add_documents([doc])
        vector_store.persist()
        print("Document added to vector store.")
        print(f"Document added: {text[:100]}...") # for testing
    except Exception as e:
        print(f"Error adding document: {e}")

def generate_response(query):
    try:
        context = retriever.get_relevant_documents(query) 
        print(f"Retrieved context: {[doc.page_content[:100] for doc in context]}") # for testing
        response = qa_chain.invoke({"question": query})
        return response['answer']
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate an answer."
