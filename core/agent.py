# core/agent.py

"""
LangChain Conversational Agent with Streaming Support

Integrates:
- User profile via system prompt
- Conversation memory
- Async token-level streaming output
- External tools support

Author: Shay Neufeld
"""

from typing import AsyncGenerator, List
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import SystemMessage

from core.model import get_llm
from core.tools import get_tools
from core.memory import get_memory
from core.profile import load_profile, create_system_message


class StreamingHandler(BaseCallbackHandler):
    """
    Callback handler to collect and yield LLM output tokens in real time.
    """
    def __init__(self):
        self.tokens: List[str] = []

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens.append(token)

    async def stream(self) -> AsyncGenerator[str, None]:
        """
        Yield tokens one-by-one as they arrive.
        """
        while True:
            while self.tokens:
                yield self.tokens.pop(0)
            # Small async sleep to avoid busy-wait
            import asyncio
            await asyncio.sleep(0.05)


async def run_agent_streaming(
    message: str,
    chat_history: List[str],
) -> AsyncGenerator[str, None]:
    """
    Run the streaming conversational agent with profile-aware context and tools.

    Args:
        message (str): User input message.
        chat_history (List[str]): Previous conversation history (for context).

    Yields:
        str: Individual output tokens from the LLM.
    """
    # Load user profile and build system prompt
    profile = load_profile()
    system_message_str = create_system_message(profile)
    system_message = SystemMessage(content=system_message_str)

    # Initialize memory with system prompt included
    memory = get_memory(system_message)

    # Streaming handler to collect tokens
    stream_handler = StreamingHandler()

    # Instantiate LLM with callbacks for streaming
    llm = get_llm(callbacks=[stream_handler])

    # Load external tools
    tools = get_tools()

    # Initialize the LangChain conversational agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,
    )

    # Run agent synchronously but tokens stream async via callback
    try:
        agent.run(message)
    except Exception as e:
        yield f"[Agent Error] {str(e)}"
        return

    # Yield tokens as they arrive
    async for token in stream_handler.stream():
        yield token
