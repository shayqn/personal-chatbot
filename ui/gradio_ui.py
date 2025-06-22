import gradio as gr
from core import chat, profile, tools, agent

# Initialize tools and agent
# Model and tools are handled inside core.agent

def respond(message, chat_name, uploaded_files):
    memory = chat.load_chat_memory(chat_name)
    memory.append({"user": message})

    # Summarize memory if too long
    if len(memory) > 10:
        memory = chat.summarize_memory(memory)

    # Compose context: profile + files + recent history
    profile_context = profile.profile_summary_for_prompt()

    # Process files (extract text)
    file_context = ""
    if uploaded_files:
        for file in uploaded_files:
            try:
                file_text = tools.extract_text_from_file(file)
            except Exception as e:
                file_text = f"[Error reading file {file.name}: {e}]"
            file_context += f"\n[File: {file.name}]\n{file_text[:2000]}\n"

    # Recent conversation history
    history_text = "\n".join(
        f"User: {m.get('user','')}\nAssistant: {m.get('assistant','')}"
        for m in memory[-5:]
    )

    full_prompt = f"{profile_context}\n{file_context}\n{history_text}\nUser: {message}"

    # Call LangChain agent for tool-enabled response
    response = agent.run_agent(full_prompt)

    memory.append({"assistant": response})
    chat.save_chat_memory(chat_name, memory)
    return response

def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# 🧠 Local LLM Assistant")

        with gr.Row():
            chat_name_input = gr.Textbox(label="Chat Name", value="default")
            new_chat_button = gr.Button("New Chat")
            load_chat_button = gr.Button("Load Chat")

        chatbot = gr.Chatbot()
        message_input = gr.Textbox(label="Your message")
        file_upload = gr.File(
            label="Attach files", file_types=[".pdf", ".txt", ".md", ".csv", ".json"], file_count="multiple"
        )
        send_button = gr.Button("Send")
        review_button = gr.Button("Review Memory")
        clear_button = gr.Button("Clear Memory")

        memory_state = gr.State([])

        def new_chat():
            chat_name_input.value = ""
            memory_state.value = []
            chatbot.clear()
            return chatbot, memory_state

        def load_chat(chat_name):
            if chat_name:
                mem = chat.load_chat_memory(chat_name)
                chat_history = []
                for m in mem:
                    if "user" in m and "assistant" in m:
                        chat_history.append((m["user"], m["assistant"]))
                memory_state.value = mem
                return chat_history, memory_state
            return [], memory_state

        def send_message(message, chat_name, files, mem):
            if not chat_name:
                return [], mem
            response = respond(message, chat_name, files)
            mem.append({"user": message})
            mem.append({"assistant": response})
            chat_history = [(m["user"], m["assistant"]) for m in mem if "user" in m and "assistant" in m]
            return chat_history, mem

        def review_memory(mem):
            return gr.Textbox.update(value=str(mem), visible=True)

        def clear_memory(chat_name):
            chat.save_chat_memory(chat_name, [])
            return [], []

        new_chat_button.click(new_chat, outputs=[chatbot, memory_state])
        load_chat_button.click(load_chat, inputs=chat_name_input, outputs=[chatbot, memory_state])
        send_button.click(send_message, inputs=[message_input, chat_name_input, file_upload, memory_state], outputs=[chatbot, memory_state])
        review_button.click(review_memory, inputs=memory_state, outputs=message_input)
        clear_button.click(clear_memory, inputs=chat_name_input, outputs=[chatbot, memory_state])

    demo.launch()
