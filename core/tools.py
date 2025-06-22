# core/tools.py

import io
import json
import csv
import PyPDF2
from typing import Any
from langchain.agents import Tool
from duckduckgo_search import DDGS

def extract_text_from_pdf(file: io.BytesIO) -> str:
    try:
        file.seek(0)
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    except Exception as e:
        return f"[PDF extraction error: {e}]"

def extract_text_from_csv(file: io.BytesIO) -> str:
    try:
        file.seek(0)
        decoded = file.read().decode('utf-8')
        reader = csv.reader(decoded.splitlines())
        rows = list(reader)
        return "\n".join([", ".join(row) for row in rows])
    except Exception as e:
        return f"[CSV extraction error: {e}]"

def extract_text_from_json(file: io.BytesIO) -> str:
    try:
        file.seek(0)
        data = json.load(file)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"[JSON extraction error: {e}]"

def extract_text_from_file(file: io.BytesIO, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".csv"):
        return extract_text_from_csv(file)
    elif filename.endswith(".json"):
        return extract_text_from_json(file)
    else:
        return "[Unsupported file format]"

def duckduckgo_search(query: str) -> str:
    """
    Perform a DuckDuckGo search and return a summary of top results.

    Args:
        query (str): Search query string.

    Returns:
        str: Formatted search results.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
        if not results:
            return "No results found."
        return "\n".join([f"- {r['title']}: {r['href']}" for r in results])
    except Exception as e:
        return f"[DuckDuckGo search error: {e}]"

def get_search_tool() -> Tool:
    """
    Returns a LangChain Tool wrapping the DuckDuckGo search function.
    """
    return Tool(
        name="DuckDuckGo Search",
        func=duckduckgo_search,
        description="Useful for answering questions by searching the internet.",
        return_direct=True,
    )
