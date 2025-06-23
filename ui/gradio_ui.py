# gradio_ui.py

import gradio as gr
from typing import List, Dict
from core.agent import run_agent_streaming

async def stream_response(user_message: str, chat_history: List[Dict[str, str]]):
    chat_history = chat_history or []

    # Append new user message
    chat_history.append({"role": "user", "content": user_message})

    # Append placeholder assistant message
    chat_history.append({"role": "assistant", "content": ""})

    # Start streaming response
    async for chunk in run_agent_streaming(chat_history):
        chat_history[-1]["content"] += chunk
        yield "", chat_history, chat_history

def clear_textbox():
    return ""

def build_ui():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(label="Conversation", height=500, show_copy_button=True, type="messages")
        user_input = gr.Textbox(placeholder="Type your message here...", show_label=False)
        submit_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear Chat")

        state = gr.State([])

        submit_btn.click(
            fn=stream_response,
            inputs=[user_input, state],
            outputs=[user_input, chatbot, state],
            queue=True
        )
        user_input.submit(  # this enables pressing "Enter" to submit
            fn=stream_response,
            inputs=[user_input, state],
            outputs=[user_input, chatbot, state],
            queue=True
        )
        submit_btn.click(fn=clear_textbox, inputs=None, outputs=user_input, queue=False)

    return demo

# gradio_ui.py

def launch_ui():
    demo = build_ui()
    demo.launch()


if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
