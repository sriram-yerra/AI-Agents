from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser

from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.tool_calling_agent import create_tool_calling_agent
from langchain.agents import AgentExecutor

from tools import search_tool, wiki_tool, save_tool

load_dotenv() # loads the .env file for fetching the API keys..!

'''
Now, I will Specify all of the fields that I want as output from my LLM call..!
'''
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# llm = ChatAnthropic(model = "claude-3-sonnet-20240229")
# llm = ChatOpenAI(model = "gpt-4o-mini")
llm = ChatOllama(model="llama3")

parser = PydanticOutputParser(pydantic_object = ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are a research assistant that will help generate a research paper. 
         Answer the user query and use necessary tools. 
         Wrap the output in this format and provide no other text\n{format_instructions}"""),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

'''
These tools were imported or Customised in the tools.py module..!
'''
tools = [search_tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools = [tools]
)

agent_executor = AgentExecutor(
    agent = agent, 
    tools = [tools], 
    verbose = True
)

# response = llm.invoke("What is the meaning of life..?")

query = input("What can i help you with today..?")
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
'''
try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print(f"Error Parsing RawResponse: ", {e})

print(structured_response.topic)

























