import gradio as gr
from agent import run_agent_streaming  # Your streaming agent generator

async def stream_response(user_message, chat_history):
    chat_history = chat_history or []

    # Append the user message with role "user"
    chat_history.append({"role": "user", "content": user_message})

    # Append an empty assistant message for streaming output
    chat_history.append({"role": "assistant", "content": ""})

    response_chunks = run_agent_streaming(user_message, chat_history)

    for chunk in response_chunks:
        # Append chunk to the last assistant message
        chat_history[-1]["content"] += chunk
        yield "", chat_history, chat_history

def clear_textbox():
    return ""

def build_ui():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(
            label="Conversation",
            height=500,
            show_copy_button=True,
            type="messages"  # <-- Use messages format here
        )
        user_input = gr.Textbox(placeholder="Type your message here...", show_label=False)
        submit_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear Chat")

        state = gr.State([])  # chat history as list of messages

        submit_btn.click(
            fn=stream_response,
            inputs=[user_input, state],
            outputs=[user_input, chatbot, state],
            queue=True,
        )
        submit_btn.click(fn=clear_textbox, inputs=None, outputs=user_input, queue=False)

        clear_btn.click(
            fn=lambda: ([], [], ""),  # reset state, chatbot and clear input
            inputs=None,
            outputs=[state, chatbot, user_input],
            queue=False,
        )

    return demo

if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
