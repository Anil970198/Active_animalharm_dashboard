import fitz  # PyMuPDF
import re
import os
from .ai import extract_violation_with_llm

def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from a PDF file.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def parse_violation(pdf_path):
    """
    Orchestrates the extraction process.
    """
    print(f"Parsing {os.path.basename(pdf_path)}...")
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return None

    # 1. Try Simple Regex (Fast, Cheap)
    # Example pattern for a date: YYYY-MM-DD or MM/DD/YYYY
    # This is a placeholder; real government PDFs are messy.
    
    # 2. Use AI for unstructured/messy data
    print("Sending text to OpenRouter for extraction...")
    data = extract_violation_with_llm(text)
    
    if data and data.get("found") is not False:
        data["source_pdf"] = os.path.basename(pdf_path)
        return data
        
    return None
