# core/agent.py

from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from core.model import get_llm
from core.tools import get_search_tool

# Initialize the language model
llm = get_llm()

# Initialize conversational memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Get tools properly wrapped as LangChain Tool objects
tools = [get_search_tool()]

# Initialize the LangChain agent with tools and memory
agent = initialize_agent(
    tools,
    llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=True,
)

def run_agent(input_text: str, chat_history: list, context_text: str = "") -> tuple[str, list]:
    """
    Runs the LangChain agent with the given input, history, and context.

    Args:
        input_text (str): The current user prompt.
        chat_history (list): List of prior conversation messages.
        context_text (str): Optional additional context.

    Returns:
        response (str): Agent's response.
        new_chat_history (list): Updated conversation history.
    """
    # Combine context with the input prompt
    if context_text:
        prompt = f"{context_text}\n\nUser: {input_text}"
    else:
        prompt = input_text

    # Run the agent and get a response
    response = agent.run(prompt)

    # Update chat history
    new_chat_history = chat_history + [(input_text, response)]

    return response, new_chat_history
