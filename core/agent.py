# agent.py

from typing import AsyncGenerator, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import initialize_agent, AgentType, Tool
from core.model import get_llm
from core.memory import get_memory
from core.tools import get_tools
from core.profile import load_profile, format_profile_as_context
from core.stream_handler import StreamingHandler  # your async callback handler


# Profile context
profile = load_profile()
system_message = SystemMessage(content=format_profile_as_context(profile))

# 🧠 Persistent memory (created once)
memory = get_memory(initial_messages=[system_message])

# ✅ Manually insert profile system message at start of memory
memory.chat_memory.messages.insert(0, system_message)

# 🛠 Tools are static, load once
tools = get_tools()

def convert_gradio_messages_to_langchain(chat_history: List[dict]) -> List:
    """
    Convert Gradio-style messages (with 'role' and 'content') into
    LangChain message objects.
    """
    messages = []
    for m in chat_history:
        role = m["role"]
        content = m["content"]
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        # system messages are handled separately via profile
    return messages


async def run_agent_streaming(chat_history: List[dict]) -> AsyncGenerator[str, None]:
    """
    Accepts full chat history in Gradio format, constructs agent with profile + memory,
    and streams token-by-token response from the agent.
    """
    # Load profile and system context
    profile = load_profile()
    system_message = SystemMessage(content=format_profile_as_context(profile))

    # Convert chat history (minus system) to LangChain messages
    lc_history = convert_gradio_messages_to_langchain(chat_history)
    
    
    
    # Setup streaming
    stream_handler = StreamingHandler()
    llm = get_llm(streaming=True, callbacks=[stream_handler])
    tools = get_tools()

    # Initialize agent with memory + tools
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        memory=memory,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    # Run the agent with the most recent user message
    last_user_message = next((m["content"] for m in reversed(chat_history) if m["role"] == "user"), None)
    if not last_user_message:
        yield "[Error: No user message found]"
        return

    try:
        agent.run(last_user_message)
    except Exception as e:
        yield f"[Agent Error] {str(e)}"
        return

    # Stream tokens from handler
    async for token in stream_handler.stream():
        yield token