# core/agent.py

from core.model import get_llm
from core.tools import get_search_tool

llm = get_llm()
search_tool = get_search_tool()

def run_agent(user_message: str, chat_history: list, extracted_text: str = "") -> tuple[str, list]:
    """
    Main agent function to process user message with chat history and optional extracted file context.

    Args:
        user_message (str): The latest user input message.
        chat_history (list): List of tuples (user, assistant) representing the conversation.
        extracted_text (str): Optional extracted content from uploaded files.

    Returns:
        response (str): Assistant's response.
        updated_chat_history (list): Updated chat history including the new exchange.
    """

    # Compose context for LLM prompt
    # You can adjust prompt formatting as needed
    context_parts = []

    if chat_history:
        # Flatten chat history into a string for context
        for i, (user_msg, assistant_msg) in enumerate(chat_history):
            context_parts.append(f"User: {user_msg}")
            context_parts.append(f"Assistant: {assistant_msg}")

    if extracted_text:
        context_parts.append(f"Extracted File Content:\n{extracted_text}")

    context_parts.append(f"User: {user_message}")

    prompt = "\n".join(context_parts) + "\nAssistant:"

    # Optionally, implement web search trigger based on user_message content or a keyword
    # For now, we keep it simple and just query the LLM with the full context
    response = llm(prompt)

    # Update chat history
    updated_chat_history = chat_history + [(user_message, response)]

    return response, updated_chat_history
