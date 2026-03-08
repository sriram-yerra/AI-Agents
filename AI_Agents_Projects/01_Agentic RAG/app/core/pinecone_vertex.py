"""
- Loads documents from folder
- Splits text into chunks
- Generates Gemini embeddings
- Uploads vectors to Pinecone (cloud DB)
- Creates searchable AI memory
- Runs once to prepare DB
Note: Retrieval happens later, NOT here.
"""

import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv("../../.env")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "quickstart"
INDEX_NAME = "pineconedb"

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_INDEX = os.getenv("PINECONE_INDEX", "pineconedb")

# GOOGLE_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
# GOOGLE_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/sriram/Documents/JSON KEYS/vectordb-486711-305adbefe017.json"

def get_pinecone_client():
    pc = Pinecone(
            api_key=os.environ["PINECONE_API_KEY"]
        )
    return pc

def get_pinecone_index():
    # INITIALIZE THE PINECONE
    pc = get_pinecone_client()
    # Create index ONLY IF it doesn't exist
    if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=768,  # Gemini text-embedding-005 output size
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    return pc

def get_index():
    pc = get_pinecone_client()
    index = pc.Index(INDEX_NAME)
    return index

def get_embeddings():
    embedding = VertexAIEmbeddings(
        model_name="text-embedding-005",
        project="vectordb-486711",
        location="us-central1"
    )
    return embedding

def get_vectordb():
    db = PineconeVectorStore.from_existing_index(
        index_name="pineconedb",
        embedding=get_embeddings()
    )
    return db

def query_pinecone(query: str, top_k: int = 3):
    vectordb = get_vectordb()
    docs = vectordb.similarity_search(query, k=top_k)
    # return clean text list
    return [doc.page_content for doc in docs]