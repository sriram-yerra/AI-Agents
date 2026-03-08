from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv("../../.env")

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("pineconedb")

# Check how many vectors exist
stats = index.describe_index_stats()
vector_count = stats.get("total_vector_count", 0)

if vector_count == 0:
    print("Pinecone index is already empty ✅")
else:
    print(f"Found {vector_count} vectors. Deleting...")
    index.delete(delete_all=True)
    print("All vectors deleted from Pinecone 🧹")
