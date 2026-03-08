'''
- Loads documents from your folder
- Splits text into smaller chunks
- Generates embeddings using Vertex/Gemini
- Stores vectors + text inside Chroma DB
- Creates searchable AI memory
- Runs once to prepare the database for retrieval
'''
'''
Note that, Here retrieval of the chunks happens, but not answering..!
'''

# https://pineconedb-uof70tx.svc.aped-4627-b74a.pinecone.io

import time
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.pinecone_vertex import get_vectordb
from pinecone import Pinecone, ServerlessSpec

loader = PyPDFDirectoryLoader("../dataSource")
data = loader.load()
print(f"Loaded {len(data)} documents")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_documents(data)
print(f"Split into {len(texts)} chunks")

vectordb = get_vectordb()

def batched(iterable, n=20):
    for i in range(0, len(iterable), n):
        yield iterable[i:i+n]

batch_size = 20
total_batches = (len(texts) + batch_size - 1) // batch_size

print(f"Processing {total_batches} batches...")

# BATCHING
for idx, batch in enumerate(batched(texts, batch_size), 1):
    try:
        get_vectordb().add_documents(batch)
        print(f"Batch {idx}/{total_batches} added")
        time.sleep(3) # To reduce the API Hits per second

    except Exception as e:
        print(f"Retrying batch {idx}: {e}")
        time.sleep(5)
        get_vectordb().add_documents(batch)

print("Pinecone DB build complete")