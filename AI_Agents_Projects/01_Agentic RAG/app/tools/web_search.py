from crewai.tools import tool
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

'''
# pip install firecrawl-py
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-7006c46beaf941a6930c8ba00c8d888a")

# Scrape a website:
app.scrape('firecrawl.dev')
'''

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool("web_search")
def web_search(query: str) -> str:
    """
    Search the internet for up-to-date information.
    Input:
        query (str): user question

    Output:
        str: summarized web results
    """
    try:
        response = firecrawl.search(query=query, limit=3)

        if not response or not response.web:
            return "No web results found."

        results_text = []

        for item in response.web:
            results_text.append(
                f"Title: {item.title}\n"
                f"URL: {item.url}\n"
                f"Description: {item.description}\n"
            )

        return "\n\n".join(results_text)

    except Exception as e:
        return f"Web search failed: {str(e)}"

    # results = firecrawl.search(query=query, limit=3)
    # print(results)   # ← add this
    # return str(results)
    
print(web_search.run("Give me some random 10 names"))