import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.scraper import fetch_url_content
from utils.parser import parse_pdf, parse_pdf_plumber, parse_docx

def test_scraper():
    url = "https://www.bbc.com/news"
    content = fetch_url_content(url)
    assert content is not None, "Failed to fetch content"
    assert len(content) > 0, "Fetched content is empty"
    print("Scraper Test passed!")

def test_parser():
    pdf_text = parse_pdf(r"tests\test.pdf")
    assert pdf_text is not None, "Failed to parse PDF with PyMuPDF"
    assert len(pdf_text) > 0, "PDF content is empty with PyMuPDF"
    print("PDF Parser (PyMuPDF) Test passed!")

    pdf_text_plumber = parse_pdf_plumber(r"tests\test.pdf")
    assert pdf_text_plumber is not None, "Failed to parse PDF with pdfplumber"
    assert len(pdf_text_plumber) > 0, "PDF content is empty with pdfplumber"
    print("PDF Parser (pdfplumber) Test passed!")

    docx_text = parse_docx(r"tests\test.docx") 
    assert docx_text is not None, "Failed to parse DOCX"
    assert len(docx_text) > 0, "DOCX content is empty"
    print("DOCX Parser Test passed!")

if __name__ == "__main__":
    test_scraper()
    test_parser()
