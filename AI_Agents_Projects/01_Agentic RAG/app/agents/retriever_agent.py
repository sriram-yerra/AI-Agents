from crewai import Agent
from tools.search_pinecone import vector_db_search
from tools.web_search import web_search
from core.llm import get_llm

def get_retriever_agent():

    response = Agent(
        role="Research Analyst",
        goal="Retrieve relevant and accurate information using available tools.",
        backstory=(
            "You are an expert research analyst. "
            "Use the vector database tool for internal knowledge. "
            "Use web search when additional or recent information is required."
        ),
        tools=[vector_db_search, web_search],
        llm=get_llm(),
        verbose=True
    )
    return response