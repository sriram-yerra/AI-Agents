from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

'''
1. Defines a Python function that saves text data into a file.
2. This lets your agent persist results instead of just printing them.
Function: 1.Formats output, 2.Adds timestamp, 3.writes to file
'''
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# Wraps function as a LangChain tool
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

'''
Provides: Real-time web search.
This creates a search utility object that can perform web searches using DuckDuckGo.

Note:
Why you needed Tool(), Because:
1. DuckDuckGoSearchRun() is just a utility class. It is not automatically a Tool
2. So you wrapped it like this: Tool(name, func, description). This converts it into a LangChain Tool object
'''
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="searchig_web",
    func=search.run,
    description="Search the web for information",
)

'''
1. This creates a wrapper around the Wikipedia API.
2. It controls how much data is fetched from Wikipedia.
3. This object acts as a controlled interface between your agent and Wikipedia:
    Fetches content, Trims it, Returns a clean summary string

Note:
1. You don’t need to wrap the Wikipedia tool with Tool() because:
2. WikipediaQueryRun is already a pre-built Tool
3. It is already implemented as a LangChain Tool internally, so it doesn’t need manual wrapping.
'''
api_wrapper = WikipediaAPIWrapper(
    top_k_results=1, 
    doc_content_chars_max=100
)
# This converts your API wrapper into a LangChain Tool that the agent can call.
wiki_tool = WikipediaQueryRun(
    api_wrapper=api_wrapper
)