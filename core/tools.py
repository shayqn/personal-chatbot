# core/tools.py

"""
LangChain-compatible tools for external actions.

Includes:
- Internet search via DuckDuckGo
- Web page content fetching
- File analysis (PDF, CSV, TXT, JSON)

These tools are available to the conversational agent when it determines external info is needed.
"""

from langchain.agents import Tool
from typing import List

from core.utils.web_utils import search_duckduckgo, fetch_page_content
from core.utils.file_utils import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_csv,
    extract_text_from_json,
)


def get_tools() -> List[Tool]:
    """
    Build and return a list of tools usable by the LangChain agent.

    Returns:
        List[Tool]: A list of LangChain-compatible Tool instances.
    """
    tools = [
        Tool(
            name="DuckDuckGo Search",
            func=lambda query: str(search_duckduckgo(query)),
            description="Useful when you need to search the internet for recent or general information.",
        ),
        Tool(
            name="Web Page Extractor",
            func=fetch_page_content,
            description="Use this to extract clean article content from a given URL.",
        ),
        Tool(
            name="Extract PDF Text",
            func=extract_text_from_pdf,
            description="Use this to extract and analyze text from a PDF file path.",
        ),
        Tool(
            name="Extract CSV Text",
            func=extract_text_from_csv,
            description="Use this to load and interpret tabular data from a CSV file path.",
        ),
        Tool(
            name="Extract TXT Text",
            func=extract_text_from_txt,
            description="Use this to extract plain text from a TXT file path.",
        ),
        Tool(
            name="Extract JSON Text",
            func=extract_text_from_json,
            description="Use this to parse and summarize the structure/content of a JSON file path.",
        ),
    ]
    return tools