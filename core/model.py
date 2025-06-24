# core/model.py

"""
Model loader using LangChain's Ollama integration.

Supports local LLMs via Ollama with optional streaming callbacks.
"""

from langchain_ollama import ChatOllama



def get_llm(streaming: bool = True, callbacks=None) -> ChatOllama:
    """
    Initialize the ChatOllama model with optional streaming.

    Args:
        model_name (str): Name of the model to load in Ollama.
        streaming (bool): Enable token-by-token streaming.
        callbacks (list): Optional list of LangChain callbacks.

    Returns:
        ChatOllama: Configured chat model instance.
    """
    return ChatOllama(
        model="llama3.2:latest",
        streaming=streaming,
        callbacks=callbacks or [],
        temperature=0.7,
    )
