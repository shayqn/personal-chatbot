# core/agent.py

"""
LangChain Conversational Agent with Streaming + Memory Support

This agent:
- Loads profile and memory
- Uses a streaming callback handler
- Yields output tokens as they are generated
"""

# core/agent.py
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage
from langchain.callbacks.base import BaseCallbackHandler

from core.model import get_llm
from core.tools import get_tools
from core.memory import get_memory
from core.profile import load_profile, format_profile_as_context

import asyncio
from typing import AsyncGenerator, List

class StreamingHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens: List[str] = []

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"[streaming token] {token}", flush=True)
        self.tokens.append(token)

    async def stream(self) -> AsyncGenerator[str, None]:
        while True:
            if self.tokens:
                yield self.tokens.pop(0)
            else:
                await asyncio.sleep(0.05)  # Prevent CPU spinning


async def run_agent_streaming(message: str) -> AsyncGenerator[str, None]:
    profile = load_profile()
    system_message = SystemMessage(content=format_profile_as_context(profile))
    memory = get_memory(initial_messages=[system_message])

    stream_handler = StreamingHandler()
    llm = get_llm(streaming=True, callbacks=[stream_handler])
    tools = get_tools()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        memory=memory,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    try:
        agent.run(message)
    except Exception as e:
        yield f"[Agent Error] {str(e)}"
        return

    async for token in stream_handler.stream():
        yield token
