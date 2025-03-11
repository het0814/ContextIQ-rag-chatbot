import fitz  # PyMuPDF
import pdfplumber
import docx

def parse_pdf(file_path):
    try:
        # Using PyMuPDF
        with fitz.open(file_path) as doc:
            text = ''
            for page in doc:
                text += page.get_text("text")
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF with PyMuPDF: {e}")
        return None

def parse_pdf_plumber(file_path):
    try:
        # Using pdfplumber for more control
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF with pdfplumber: {e}")
        return None

def parse_docx(file_path):
    try:
        # Using python-docx
        doc = docx.Document(file_path)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text.strip()
    except Exception as e:
        print(f"Error parsing DOCX file: {e}")
        return None
