import os
import json
from typing import List, Dict
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from core.model import get_llm

CHAT_DIR = os.path.join("data", "chats")
os.makedirs(CHAT_DIR, exist_ok=True)

def get_chat_path(chat_name: str) -> str:
    return os.path.join(CHAT_DIR, f"{chat_name}.json")

def load_chat_memory(chat_name: str) -> List[Dict]:
    path = get_chat_path(chat_name)
    return json.load(open(path)) if os.path.exists(path) else []

def save_chat_memory(chat_name: str, memory: List[Dict]):
    with open(get_chat_path(chat_name), "w") as f:
        json.dump(memory, f, indent=2)

def list_chats() -> List[str]:
    return [f[:-5] for f in os.listdir(CHAT_DIR) if f.endswith(".json")]

def summarize_memory(memory: List[Dict]) -> List[Dict]:
    if not memory:
        return []
    full_text = "\n".join(
        f"User: {m['user']}\nAssistant: {m.get('assistant', '')}" for m in memory if 'user' in m
    )
    docs = [Document(page_content=full_text)]
    llm = get_llm()
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run(docs)
    return [{"system": f"Conversation summary: {summary}"}]
