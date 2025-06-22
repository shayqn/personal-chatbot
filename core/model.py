'''
from langchain_community.llms import Ollama


MODEL_NAME = "llama3"  # Change here to swap models (e.g. "mistral", "phi3")

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = Ollama(model=MODEL_NAME)
    return _llm


def get_llm():
    return Ollama(model="llama3.2:latest", server_url="http://localhost:11434")
'''

from langchain_ollama import OllamaLLM

def get_llm():
    return OllamaLLM(model="llama3.2:latest", base_url="http://localhost:11434")
