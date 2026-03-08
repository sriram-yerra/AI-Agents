from crewai.tools import tool
from app.core.pinecone_vertex import query_pinecone

# Takes user query, calls Pinecone, returns context text
# This becomes a Tool the agent can call
@tool("vector_db_search")
def vector_db_search(query: str) -> str:
    '''
    Search the Pinecone vector database for relevant information.
    Input:
        query (str): user question
    Output:
        str: concatenated relevant context from vector DB
    '''
    results = query_pinecone(query)
    if not results:
        return "No relevant documents found in the knowledge base."
    return "\n\n".join(results)

