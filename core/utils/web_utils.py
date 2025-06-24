#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 12:38:08 2025

@author: shayneufeld
"""

# core/utils/web_utils.py

"""
Utilities for performing internet search and web content extraction.

Supports:
- DuckDuckGo search (via duckduckgo-search)
- Web page scraping and summarization (via readability + BeautifulSoup)

These are used by agent tools to retrieve external knowledge when needed.
"""

from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from readability import Document
from typing import List, Dict


def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a DuckDuckGo search and return top results.

    Args:
        query (str): Search string.
        max_results (int): Maximum number of results to return.

    Returns:
        List[Dict]: Each dict contains 'title', 'href', and 'body'.
    """
    with DDGS() as ddgs:
        results = ddgs.text(query)
        return [
            {"title": r["title"], "href": r["href"], "body": r["body"]}
            for i, r in enumerate(results)
            if i < max_results
        ]


def fetch_page_content(url: str) -> str:
    """
    Fetch and extract clean main content from a web page.

    Args:
        url (str): Target URL.

    Returns:
        str: Extracted readable content from the page.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        doc = Document(response.text)
        html = doc.summary()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()
    except Exception as e:
        return f"[Error fetching page] {str(e)}"
