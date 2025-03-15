import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.scraper import fetch_url_content
from utils.parser import parse_pdf, parse_pdf_plumber, parse_docx
from retrieval.retriever import add_document, generate_response

def test_scraper():
    url = "https://www.bbc.com/news"
    content = fetch_url_content(url)
    assert content is not None, "Failed to fetch content"
    assert len(content) > 0, "Fetched content is empty"
    print("Scraper Test passed!")
    print(content)

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

def test_generate_response():
    sample_text = "OpenAI develops powerful language models like GPT-4."
    add_document(sample_text, {"source": "test"})

    # Test single query
    query = "Who develops GPT-4?"
    response = generate_response(query)
    assert response is not None, "Failed to generate response"
    assert len(response) > 0, "Generated response is empty"
    assert "OpenAI" in response, "Response doesn't contain expected content"
    print("Single Query Test passed!")

    # Test follow-up query to check context retention
    follow_up_query = "What other models have they created?"
    follow_up_response = generate_response(follow_up_query)
    print(follow_up_response)
    assert follow_up_response is not None, "Failed to generate follow-up response"
    assert len(follow_up_response) > 0, "Generated follow-up response is empty"
    assert "GPT" in follow_up_response, "Expected context not found in follow-up response"
    print("Follow-Up Query Test passed!")


if __name__ == "__main__":
    test_scraper()
    test_parser()
    test_generate_response()
