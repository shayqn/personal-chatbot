from langchain_community.llms import Ollama

MODEL_NAME = "llama3"  # Change here to swap models (e.g. "mistral", "phi3")

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = Ollama(model=MODEL_NAME)
    return _llm
