from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.scraper import fetch_url_content
from utils.parser import parse_pdf, parse_pdf_plumber, parse_docx
from retrieval.retriever import add_document, generate_response
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",  # allows request only from frontend (React app)
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

class URLRequest(BaseModel):
    url: str

class ResponseRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "ContextIQ RAG Chatbot is running!"}

@app.post("/add-url")
def add_url(request: URLRequest):
    try:
        content =  fetch_url_content(request.url)
        if not content:
            raise HTTPException(status_code=400, detail="Failed to fetch content from URL.")
        
        add_document(content, metadata={"source": request.url})
        return {"message": "URL content added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding URL content: {e}")

@app.post("/upload-document")
async def upload_document(file: UploadFile):
    try:
        filename = file.filename
        extension = os.path.splitext(filename)[1].lower()

        content = None
        if extension == ".pdf":
            content = parse_pdf(file.file) or parse_pdf_plumber(file.file)
        elif extension == ".docx":
            content = parse_docx(file.file)
        elif extension == ".txt":
            content = await file.read()
            content = content.decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")
        
        if not content:
            raise HTTPException(status_code=400, detail="Failed to extract content from file.")
        
        add_document(content, metadata={"source": filename})
        return {"message": f"{filename} content added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding document: {e}")

@app.post("/generate-response")
def generate_response_endpoint(request: ResponseRequest):
    try:
        response = generate_response(request.query)
        if not response:
            raise HTTPException(status_code=404, detail="Failed to generate response.")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")


