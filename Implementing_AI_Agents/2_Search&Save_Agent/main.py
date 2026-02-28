from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.tool_calling_agent import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_google_vertexai import ChatVertexAI

from tools import search_tool, wiki_tool, save_tool

load_dotenv("../.env")

'''
Now, I will Specify all of the fields that I want as output from my LLM call..!
Defines a structured output format
This ensures LLM output is consistent and machine-readable
'''
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# -------------------------
# GEMINI LLM
# -------------------------
llm = ChatVertexAI(
    model_name=os.getenv("GEMINI_MODEL"),
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_REGION"),
    temperature=float(os.getenv("TEMPERATURE")),
    max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS")),
)

'''
Takes LLM output text
Converts into ResearchResponse object
Also generates format instructions used in prompt
'''
parser = PydanticOutputParser(pydantic_object = ResearchResponse)

'''
You define multi-message prompt:
'''
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", # It tells LLM exact JSON schema format
         """You are a research assistant that will help generate a research paper. 
         Answer the user query and use necessary tools. 
         Wrap the output in this format and provide no other text\n{format_instructions}"""),
        ("placeholder", "{chat_history}"),     # Reserved for memory (conversation history)
        ("human", "{query}"),                  # User input will be injected here
        ("placeholder", "{agent_scratchpad}"), # This is used internally to store: 1. tool calls, 2. intermediate steps
    ]

  # This fills the placeholder with: schema instructions from parser
).partial(format_instructions=parser.get_format_instructions()) 

'''
These tools were imported or Customised in the tools.py module..!
This list defines: All tools agent can use
'''
tools = [search_tool, wiki_tool, save_tool]

# Create Agent
agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools = [tools]
)

# Create Agent Executor
agent_executor = AgentExecutor(
    agent = agent, 
    tools = [tools], 
    verbose = True
)

# response = llm.invoke("What is the meaning of life..?")

# Takes input from user
query = input("What can i help you with today..?")

# Invoke Agent
raw_response = agent_executor.invoke(
    {
        # "query": "Whatt is the capital of France..?",
        "query": query,
        "name": "SriRam's Query"
    }
)
print(raw_response)

'''
To avoid the risk of failing, I used try block..!
Parse Structured Output, then converting to: ResearchResponse object
'''
# structured_response = parser.parse(raw_response.get("output")[0]["text"])
# print(structured_response)
try:
    
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print(f"Error Parsing RawResponse: ", {e})

print(structured_response.topic)

























