"""
ReAct agent setup for document retrieval and question answering.
"""

import os

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import Config
from src.llms.openai import llm
from src.rag.retriever_setup import get_retriever

config = Config()

def get_agent_executor(user_id: str) -> AgentExecutor:
    """
    Get a user-scoped ReAct agent executor.
    
    Args:
        user_id: The ID of the authenticated user.
        
    Returns:
        An AgentExecutor instance configured with user-scoped tools.
    """
    # Initialize tools with user context
    tools = [get_retriever(user_id)]

    # Load document description if available
    if os.path.exists("description.txt"):
        with open("description.txt", "r", encoding="utf-8") as f:
            description = f.read()
    else:
        description = None

    # Create ReAct agent prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", config.prompt("system_prompt")),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}")
    ])

    # Initialize the ReAct agent and executor
    react_agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=react_agent,
        tools=tools,
        handle_parsing_errors=True,
        max_iterations=2,
        verbose=True,
        return_intermediate_steps=True
    )
    
    return agent_executor

