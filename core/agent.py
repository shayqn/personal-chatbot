# local_llm_assistant/core/agent.py

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from core import tools, model

def search_tool_func(query: str) -> str:
    search = tools.get_search_tool()
    return search(query)

search_tool = Tool(
    name="Web Search",
    func=search_tool_func,
    description="Useful for answering questions by searching the internet."
)

def file_analysis_tool_func(text: str) -> str:
    # Simple echo or limited summary of file content; expand as needed
    snippet = text[:1000]
    return f"File content preview (first 1000 chars):\n{snippet}"

file_analysis_tool = Tool(
    name="File Analyzer",
    func=file_analysis_tool_func,
    description="Analyzes and summarizes text extracted from uploaded files."
)

llm = model.get_llm()

agent = initialize_agent(
    tools=[search_tool, file_analysis_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

def run_agent(prompt: str) -> str:
    return agent.run(prompt)
