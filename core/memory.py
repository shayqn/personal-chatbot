# core/memory.py

"""
Conversation Memory Management

Provides a reusable function to create and return
a LangChain ConversationBufferMemory instance
initialized with an optional system message.

Author: Shay Neufeld
"""

from typing import Optional
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage


def get_memory(system_message: Optional[SystemMessage] = None) -> ConversationBufferMemory:
    """
    Create a conversation memory buffer.

    Args:
        system_message (Optional[SystemMessage]): Initial system message to prime memory.

    Returns:
        ConversationBufferMemory: Memory instance maintaining chat history.
    """
    initial_messages = [system_message] if system_message else []
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        initial_messages=initial_messages,
    )
    return memory
