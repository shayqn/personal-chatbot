# local_llm_assistant/core/tools.py

import io
import json
import pandas as pd
import fitz  # PyMuPDF
from duckduckgo_search import ddg

def get_search_tool():
    """
    Returns a simple search function that queries DuckDuckGo
    and returns top 3 results summaries as text.
    """
    def search(query: str, max_results: int = 3):
        results = ddg(query, max_results=max_results)
        summaries = []
        if results:
            for res in results:
                title = res.get("title", "")
                snippet = res.get("body", "")
                url = res.get("href", "")
                summaries.append(f"{title}\n{snippet}\n{url}")
        return "\n\n".join(summaries) if summaries else "No results found."
    return search

def extract_text_from_pdf(file: io.BytesIO) -> str:
    """Extract text from PDF using PyMuPDF, preserving layout where possible."""
    try:
        file.seek(0)
        doc = fitz.open(stream=file.read(), filetype="pdf")
        texts = [page.get_text("text") for page in doc]
        return "\n".join(texts)
    except Exception as e:
        return f"[PDF extraction error: {e}]"

def extract_text_from_csv(file: io.BytesIO) -> str:
    """Load CSV, validate, and return a string summary of columns and sample rows."""
    try:
        file.seek(0)
        df = pd.read_csv(file)
        sample = df.head(5).to_string()
        columns = ", ".join(df.columns)
        return f"CSV columns: {columns}\nSample data:\n{sample}"
    except Exception as e:
        return f"[CSV extraction error: {e}]"

def extract_text_from_json(file: io.BytesIO) -> str:
    """Load JSON and pretty-print with indentation."""
    try:
        file.seek(0)
        data = json.load(file)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"[JSON extraction error: {e}]"

def extract_text_from_txt(file: io.BytesIO) -> str:
    """Read plain text or markdown files."""
    try:
        file.seek(0)
        return file.read().decode("utf-8")
    except Exception as e:
        return f"[Text extraction error: {e}]"

def extract_text_from_file(file) -> str:
    """
    Master file extractor that dispatches by file type.
    Accepts file-like object with a .name attribute.
    """
    filename = file.name.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".csv"):
        return extract_text_from_csv(file)
    elif filename.endswith(".json"):
        return extract_text_from_json(file)
    elif filename.endswith((".txt", ".md")):
        return extract_text_from_txt(file)
    else:
        return "[Unsupported file type for extraction]"
