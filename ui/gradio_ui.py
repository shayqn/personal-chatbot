# gradio_ui.py

import gradio as gr
from typing import List, Dict
from core.agent import run_agent_streaming
        
import asyncio

# Step 1: Add the user message and placeholder assistant message
def submit_user_message(user_message: str, chat_history: List[Dict[str, str]]):
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": ""})
    return "", chat_history, chat_history

# Step 2: Stream the assistant response
async def stream_bot_response(chat_history: List[Dict[str, str]]):
    async for chunk in run_agent_streaming(chat_history):
        chat_history[-1]["content"] += chunk
        yield "", chat_history, chat_history

def clear_textbox():
    return ""

def build_ui():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(label="Conversation", height=500, show_copy_button=True, type="messages")

        user_input = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            lines=1,
            autofocus=True
        )

        submit_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear Chat")
        state = gr.State([])

        # Step 1: Add user message immediately
        submit_btn.click(
            fn=submit_user_message,
            inputs=[user_input, state],
            outputs=[user_input, chatbot, state],
            queue=False
        )

        user_input.submit(
            fn=submit_user_message,
            inputs=[user_input, state],
            outputs=[user_input, chatbot, state],
            queue=False
        )

        # Step 2: Begin streaming after UI updates
        submit_btn.click(
            fn=stream_bot_response,
            inputs=[state],
            outputs=[user_input, chatbot, state],
            queue=True
        )

        user_input.submit(
            fn=stream_bot_response,
            inputs=[state],
            outputs=[user_input, chatbot, state],
            queue=True
        )

        # Clear user input after submission
        submit_btn.click(fn=clear_textbox, inputs=None, outputs=user_input, queue=False)
        user_input.submit(fn=clear_textbox, inputs=None, outputs=user_input, queue=False)

        # Clear everything
        clear_btn.click(
            fn=lambda: ([], [], ""),
            inputs=None,
            outputs=[state, chatbot, user_input],
            queue=False
        )

    return demo

def launch_ui():
    demo = build_ui()
    demo.launch()


if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
