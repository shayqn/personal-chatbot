# core/tools.py

import io
import asyncio
import json
from typing import Optional, Union, Any
import fitz  # PyMuPDF
import pandas as pd
from typing import List, Dict
from duckduckgo_search import DDGS

FileInput = Union[str, io.BytesIO]

def extract_text_from_pdf(file: FileInput) -> str:
    """
    Extract all text from a PDF file.
    
    Args:
        file: Path to PDF file (str) or a file-like object (io.BytesIO).
    
    Returns:
        Extracted text as a string, or error message on failure.
    """
    try:
        if isinstance(file, str):
            doc = fitz.open(file)
        else:
            file.seek(0)
            doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"[PDF extraction error: {e}]"

def extract_text_from_csv(file: FileInput) -> str:
    """
    Extract text content from a CSV file.
    
    Args:
        file: Path to CSV file (str) or a file-like object (io.BytesIO).
    
    Returns:
        CSV contents as a string table, or error message on failure.
    """
    try:
        if isinstance(file, str):
            df = pd.read_csv(file)
        else:
            file.seek(0)
            df = pd.read_csv(file)
        return df.to_string()
    except Exception as e:
        return f"[CSV extraction error: {e}]"

def extract_text_from_json(file: FileInput) -> str:
    """
    Load JSON from file or file-like object and pretty-print with indentation.
    
    Args:
        file: Path to JSON file (str) or a file-like object (io.BytesIO).
    
    Returns:
        JSON pretty string, or error message on failure.
    """
    try:
        if isinstance(file, str):
            with open(file, "r") as f:
                data = json.load(f)
        else:
            file.seek(0)
            data = json.load(file)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"[JSON extraction error: {e}]"

def extract_text_from_file(file: FileInput) -> Optional[str]:
    """
    Detect file type from extension (if path) or fallback to JSON extraction,
    then extract text using the appropriate extractor.
    
    Args:
        file: Path to file (str) or file-like object (io.BytesIO).
    
    Returns:
        Extracted text string or None if unsupported.
    """
    try:
        # Determine extension if possible
        ext = None
        if isinstance(file, str):
            ext = file.lower().split('.')[-1]
        else:
            # If file-like object, try to guess by checking header bytes for PDF or fallback to JSON
            # For simplicity, just try JSON extraction as fallback
            ext = None

        if ext == "pdf":
            return extract_text_from_pdf(file)
        elif ext == "csv":
            return extract_text_from_csv(file)
        elif ext == "json":
            return extract_text_from_json(file)
        else:
            # If unknown extension or file-like object, try JSON extraction as a safe fallback
            return extract_text_from_json(file)
    except Exception as e:
        return f"[File extraction error: {e}]"


def get_search_tool():
    """
    Returns a synchronous search function that queries DuckDuckGo using
    the asynchronous DDGS client from the duckduckgo_search v8.x library.

    The returned function takes a query string and max_results integer,
    performs the search asynchronously, and returns a formatted summary string
    of the top results.

    Returns:
        function: A synchronous search function with signature (query: str, max_results: int) -> str
    """

    def search(query: str, max_results: int = 3) -> str:
        """
        Performs a DuckDuckGo search for the given query and returns
        a summarized string of results.

        Args:
            query (str): Search query string.
            max_results (int): Maximum number of results to retrieve (default 3).

        Returns:
            str: Formatted string with titles, snippets, and URLs of search results,
                 or "No results found." if none.
        """

        async def async_search() -> List[Dict]:
            results = []
            try:
                async with DDGS() as client:
                    async for result in client.text(query, max_results=max_results):
                        results.append(result)
            except Exception as e:
                # Log or handle exceptions as needed
                print(f"[DuckDuckGo search error]: {e}")
            return results

        # Run the async search synchronously
        results = asyncio.run(async_search())

        if not results:
            return "No results found."

        # Format results into readable summaries
        summaries = []
        for res in results:
            title = res.get("title", "").strip()
            snippet = res.get("body", "").strip()
            url = res.get("href", "").strip()
            entry = f"{title}\n{snippet}\n{url}"
            summaries.append(entry)

        return "\n\n".join(summaries)

    return search

