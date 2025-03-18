from langchain_community.vectorstores import Chroma 
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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

# Custom Prompt Template
prompt_template = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template="""
    You are a helpful and knowledgeable AI assistant.

    Use the following context and previous conversation to answer the user's question:

    Previous conversation:
    {chat_history}

    Context:
    {context}

    - If the context doesn’t provide enough information, say you don’t know instead of guessing.  
    - Keep answers clear, concise, and directly relevant to the question.  
    - When helpful, use bullet points or lists to improve clarity.  

    Question: {question}

    Answer:
    """
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt_template}
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

def context_sources():
    try:
        # Retrieve all context sources from the vector store
        results = vector_store.get()
        metadatas = results.get("metadatas", [])
        context_sources = [
            {"source": metadata.get("source", "Unnamed document")}
            for metadata in metadatas
        ]
        return context_sources
    except Exception as e:
        print(f"Error getting context sources: {e}")