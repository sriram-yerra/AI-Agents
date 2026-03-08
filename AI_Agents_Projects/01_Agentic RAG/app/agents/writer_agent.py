from crewai import Agent
from core.llm import get_llm

def get_writer_agent():
    response = Agent(
        role="Technical Writer",
        goal="Generate a clear, concise, and accurate answer based on the retrieved insights.",
        backstory=(
            "You are a professional technical writer. "
            "Use the research insights provided to produce a structured and high-quality answer."
        ),
        llm=get_llm(),
        verbose=True
    )
    return response