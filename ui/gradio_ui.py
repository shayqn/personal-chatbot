# ui/gradio_ui.py

"""
Gradio Chat UI for Local LLM Assistant with Async Streaming

Features:
- Streams bot response tokens as they arrive
- Displays full conversation history
- Immediate user message display and input clearing

Author: Shay Neufeld
"""

from typing import List, Tuple, AsyncGenerator
import gradio as gr
from core.agent import run_agent_streaming

ChatHistory = List[Tuple[str, str]]  # (user_message, bot_message)


async def stream_response(
    user_message: str, history: ChatHistory
) -> AsyncGenerator[Tuple[ChatHistory, ChatHistory], None]:
    """
    Async generator that yields chat history updates as new tokens arrive.

    Args:
        user_message (str): The user's input message.
        history (ChatHistory): Current chat history.

    Yields:
        Tuple[ChatHistory, ChatHistory]: Updated chat history for display and state.
    """
    # Immediately append user's message with empty bot response
    history = history + [(user_message, "")]

    # Stream tokens from agent
    async for token in run_agent_streaming(user_message, history):
        user_msg, bot_msg = history[-1]
        bot_msg += token
        history[-1] = (user_msg, bot_msg)

        # Yield updated history twice (once for display, once for state)
        yield history, history


def launch_ui():
    """
    Initialize and launch the Gradio UI.
    """
    with gr.Blocks() as demo:
        gr.Markdown("# Local LLM Assistant")

        chatbot = gr.Chatbot(elem_id="chatbot").style(height=600)
        state = gr.State([])  # Stores chat history

        user_input = gr.Textbox(
            placeholder="Enter message here...",
            label="Your message",
            lines=2,
            max_lines=5,
        )

        # Submit handler: stream_response streams tokens, updates chatbot and state
        user_input.submit(
            fn=stream_response,
            inputs=[user_input, state],
            outputs=[chatbot, state],
            stream=True,
        )

        # Clear input after submit for UX
        user_input.submit(lambda: "", None, user_input)

    demo.launch()


if __name__ == "__main__":
    launch_ui()
