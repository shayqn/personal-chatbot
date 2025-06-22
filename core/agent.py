# core/agent.py

"""
Agent module for the local LLM assistant.

This module sets up and runs a LangChain conversational agent
that integrates user profile context, memory, and external tools
such as web search. It manages the conversation memory with
a system role message containing the user profile to provide
personalized and context-aware responses.

Key functions:
- create_system_message: Generate system prompt from user profile
- run_agent: Run the agent with input message, memory, and tools
"""

from typing import List, Tuple, Any

from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage, AIMessage
from core.model import get_llm
from core.tools import get_tools
from core.profile import load_profile




def create_system_message(profile: dict) -> str:
    """
    Build a system message string incorporating user profile info.

    Args:
        profile (dict): User profile loaded from profile.json

    Returns:
        str: System prompt describing user info and behavior instructions
    """
    interests = ", ".join(profile.get("interests", []))
    style = profile.get("preferences", {}).get("response_style", "")
    name = profile.get("name", "User")

    system_msg = (
        "You are a helpful assistant. "
        "Use the following information to personalize your responses:\n"
        f"User's name: {name}\n"
        f"Interests: {interests}\n"
        f"Preferred response style: {style}\n"
        "You should only use external tools like search if the user's question requires "
        "information beyond what you confidently know or the user profile.\n"
        "For personal or common knowledge questions, answer directly and clearly without searching.\n"
    )
    return system_msg


def run_agent(message: str, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Process a user message through the LangChain agent with memory and tools.

    Args:
        message (str): The user's input message
        chat_history (List[Tuple[str, str]]): The current conversation history

    Returns:
        Tuple[str, List[Tuple[str, str]]]: Agent's response and updated chat history
    """

    # Load profile info and generate system prompt
    profile = load_profile()
    system_message_str = create_system_message(profile)

    # Setup memory and replay past conversation into memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        initial_messages=[SystemMessage(content=system_message_str)],
    )

    # Rebuild memory with prior chat messages
    for user_msg, bot_msg in chat_history:
        memory.chat_memory.add_user_message(user_msg)
        memory.chat_memory.add_ai_message(bot_msg)

    # Load LLM and tools
    llm = get_llm()
    tools = get_tools()

    # Initialize agent with memory
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
    )

    # Generate response
    response = agent.run(input=message)

    # Append latest interaction to chat history
    updated_history = chat_history + [(message, response)]

    return response, updated_history
