"""
gradio_ui.py

Defines the Gradio-based user interface for interacting with the chatbot agent.
Maintains chat history state and manages user input/output flows.

Requires:
- core.agent.run_agent(message: str, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]

Author: Shay Neufeld (adapted)
Date: 2025-06-22
"""

import gradio as gr
from typing import List, Tuple

from core.agent import run_agent

def chat_with_agent(
    message: str,
    chat_history: List[Tuple[str, str]]
) -> Tuple[List[List[str]], List[Tuple[str, str]]]:
    """
    Process user input through the chatbot agent and update conversation history.

    Args:
        message (str): The new user message to process.
        chat_history (List[Tuple[str, str]]): Existing conversation as list of (user_msg, bot_msg) tuples.

    Returns:
        Tuple[List[List[str]], List[Tuple[str, str]]]:
            - Updated chat history formatted as a list of [user_msg, bot_msg] lists (for Gradio UI).
            - Updated internal chat history as list of tuples for state management.
    """
    # Run the agent to get response and updated history
    response, updated_history = run_agent(message, chat_history)

    # Convert tuple-based history to list-of-lists for Gradio Chatbot compatibility
    gradio_history = [[user, bot] for user, bot in updated_history]

    return gradio_history, updated_history

def launch_ui():
    """
    Launches the Gradio web UI, setting up chatbot interface, inputs, and event handlers.
    """
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(label="Personal Assistant Chatbot")
        user_input = gr.Textbox(
            label="Enter your message",
            placeholder="Type your message here and press Enter"
        )
        clear_button = gr.Button("Clear Conversation")

        # State to hold the chat history as List[Tuple[str, str]]
        chat_state = gr.State([])

        # Submit handler: send user input and history to agent, update UI
        def on_submit(message, history):
            return chat_with_agent(message, history)

        # Bind submit and clear button events
        user_input.submit(on_submit, inputs=[user_input, chat_state], outputs=[chatbot, chat_state])
        clear_button.click(lambda: ([], []), inputs=None, outputs=[chatbot, chat_state])

    demo.launch()

if __name__ == "__main__":
    launch_ui()
