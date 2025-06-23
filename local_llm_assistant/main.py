# local_llm_assistant/main.py

"""
Main entry point for the personal chatbot with local LLM + internet tools.

Launches the Gradio UI interface and connects to the full backend pipeline.
"""

from ui.gradio_ui import launch_ui

if __name__ == "__main__":
    launch_ui()
