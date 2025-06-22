# core/tools.py

"""
Tools module for the local LLM assistant.

This module provides utility functions wrapped as LangChain Tools
to be used by the conversational agent. It includes file content
extractors and an internet search tool.

Key functions:
- extract_text_from_file: Extract text content from uploaded files (txt, json, pdf)
- search_web: Perform DuckDuckGo web search and return summaries
- get_tools: Return a list of LangChain Tool objects for the agent
"""

import io
import json
from typing import List, Any

from langchain.tools import Tool

from duckduckgo_search import DDGS

from PyPDF2 import PdfReader


def extract_text_from_file(file: io.BytesIO) -> str:
    """
    Extract text content from a given file-like object.

    Supports text, JSON, and PDF files based on simple heuristics.

    Args:
        file (io.BytesIO): In-memory file object

    Returns:
        str: Extracted text content or error message
    """
    try:
        file.seek(0)
        # Try text decoding first
        content = file.read()
        try:
            text = content.decode("utf-8")
            return text
        except UnicodeDecodeError:
            # Try JSON parsing
            file.seek(0)
            data = json.load(file)
            return json.dumps(data, indent=2)
    except Exception:
        # If not text or JSON, try PDF extraction
        try:
            file.seek(0)
            reader = PdfReader(file)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n\n".join(pages)
        except Exception as e:
            return f"[Error extracting text: {e}]"


def search_web(query: str, max_results: int = 3) -> str:
    """
    Perform a DuckDuckGo web search and return formatted result snippets.

    Args:
        query (str): Search query string
        max_results (int): Number of results to return (default 3)

    Returns:
        str: Concatenated titles and snippets of search results
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if not results:
                return "[No search results found.]"
            snippets = []
            for r in results:
                title = r.get("title", "No title")
                snippet = r.get("body", "No snippet")
                snippets.append(f"Title: {title}\nSnippet: {snippet}\n")
            return "\n".join(snippets)
    except Exception as e:
        return f"[Search error: {e}]"


def get_tools() -> List[Tool]:
    """
    Return a list of LangChain Tool instances to be used by the agent.

    Includes:
    - web_search: DuckDuckGo search tool
    - extract_text: File text extraction tool

    Returns:
        List[Tool]: List of tool objects
    """

    def extract_text_tool(file: io.BytesIO) -> str:
        # Wrapper to adapt signature for Tool usage
        return extract_text_from_file(file)

    web_search_tool = Tool(
        name="web_search",
        func=search_web,
        description="Useful for answering questions about recent events or "
        "specific information not known from training or user profile."
        "Only use if the question cannot be answered confidently otherwise",
    )

    extract_text_tool_obj = Tool(
        name="extract_text",
        func=extract_text_tool,
        description="Extract text content from an uploaded file (txt, json, pdf).",
    )

    return [web_search_tool, extract_text_tool_obj]

