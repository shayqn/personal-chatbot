# ui/gradio_ui.py

import gradio as gr
from core.tools import extract_text_from_file
from core.agent import run_agent  # Assumes this accepts (message, history, context) and returns (response, new_history)

def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("## Local LLM Chatbot with File Upload and Web Search")

        chatbot = gr.Chatbot(label="Chat History")
        file_input = gr.File(label="Upload a file (PDF, CSV, JSON)", file_types=[".pdf", ".csv", ".json"])
        extracted_text_output = gr.Textbox(label="Extracted File Content", interactive=False, lines=10)

        user_input = gr.Textbox(label="Your message", placeholder="Type your message here...")

        def handle_file_upload(file_obj):
            if file_obj is None:
                return ""
            # file_obj is a tempfile.NamedTemporaryFile with .name attribute
            # We pass the file path to extract_text_from_file
            try:
                extracted_text = extract_text_from_file(file_obj.name)
            except Exception as e:
                extracted_text = f"[Error extracting file: {e}]"
            return extracted_text

        file_input.change(fn=handle_file_upload, inputs=file_input, outputs=extracted_text_output)

        def chat_with_agent(message, chat_history, extracted_text):
            if chat_history is None:
                chat_history = []
            response, new_history = run_agent(message, chat_history, extracted_text)
            # Append user message and bot response to chat history for display
            updated_history = new_history
            return updated_history, updated_history

        user_input.submit(
            chat_with_agent,
            inputs=[user_input, chatbot, extracted_text_output],
            outputs=[chatbot, chatbot],
            api_name="chat"
        )

    demo.launch()
