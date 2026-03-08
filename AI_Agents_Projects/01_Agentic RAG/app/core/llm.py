from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv
from agents.retriever import retriever
import sys

load_dotenv()

# LLM (Vertex Gemini) 
def get_llm():
    """
    Initialize and return Gemini LLM via VertexAI
    This LLM will be used inside CrewAI agents.
    """
    llm = ChatVertexAI(
        model_name="gemini-1.5-pro",   # or gemini-pro
        temperature=0.2,
        max_output_tokens=1024
    )
    return llm

template = """
Answer the question based only on the context below, read the content provided by rag pipeline and give me a wise output.
Context:
{context}
Question:
{question}
"""
# prompt = ChatPromptTemplate.from_template(template)

# Format retrieved docs into text
def format_docs(docs):
    # for doc in docs:
    #     "\n".join(doc.page_content)
    return "\n".join(doc.page_content for doc in docs)

'''
What is a “Chain” here?
A chain = a pipeline of steps where output of one step becomes input of the next.
LangChain Expression Language (LCEL)
'''

# RAG Chain (LCEL): First Version (LCEL / Runnable Chain)
# rag_chain = (
#     {
#         "context": retriever | RunnableLambda(format_docs),  # retriever → text
#         "question": RunnablePassthrough()
#     }
#     | prompt
#     | get_llm()
#     | StrOutputParser()
# )

# Function to print sources 
# def process_llm_response(answer, query):
#     print("\nANSWER:\n")
#     print(answer)

#     print("\nSOURCES:\n")
#     docs = retriever.invoke(query)
#     for doc in docs:
#         print(doc.metadata["source"])

# def Query():
#     while True:
#         user_input = input(f"Input Prompt: ")
#         if user_input == 'exit':
#             print('Exiting')
#             sys.exit()
#         if user_input == '':
#             continue
#         answer = rag_chain.invoke(user_input)
#         process_llm_response(answer, user_input)
#         # print(f"Answer: {result['result']}")

# Query()