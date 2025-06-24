# core/memory.py

"""
Conversation Memory Setup

Uses buffer memory with support for a persistent system message.

Author: Shay Neufeld
"""

from langchain.memory import ConversationBufferMemory
from typing import Optional, List
from langchain_core.messages import BaseMessage


def get_memory(initial_messages: Optional[List[BaseMessage]] = None):
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="input",
        output_key="output",
        initial_messages=initial_messages or [],
    )
