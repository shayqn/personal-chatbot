# core/tools.py

"""
Tool Definitions for Conversational Agent

Includes external tool wrappers and utility extraction tools.
All tools are returned from get_tools() to be loaded by the agent.

Author: Shay Neufeld
"""

from typing import List
from langchain.tools import Tool
from langchain.utilities import DuckDuckGoSearchAPIWrapper


def duckduckgo_search_tool() -> Tool:
    """
    Create a DuckDuckGo Search tool instance.

    Returns:
        Tool: LangChain Tool wrapping DuckDuckGo Search.
    """
    search = DuckDuckGoSearchAPIWrapper()
    return Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Useful for answering questions about current events or general knowledge."
    )


def get_tools() -> List[Tool]:
    """
    Return all tools available to the agent.

    Returns:
        List[Tool]: List of LangChain tools.
    """
    return [
        duckduckgo_search_tool(),
        # Add other tools here if you create extraction or file handling tools later
    ]
