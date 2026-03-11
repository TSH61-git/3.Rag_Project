import os
from dotenv import load_dotenv

load_dotenv()

print("Checking API keys...")
print(f"COHERE_API_KEY: {os.getenv('COHERE_API_KEY')[:10]}..." if os.getenv('COHERE_API_KEY') else "COHERE_API_KEY: NOT FOUND")
print(f"PINECONE_API_KEY: {os.getenv('PINECONE_API_KEY')[:10]}..." if os.getenv('PINECONE_API_KEY') else "PINECONE_API_KEY: NOT FOUND")

# Test Cohere connection
try:
    import cohere
    co = cohere.Client(os.getenv('COHERE_API_KEY'))
    response = co.embed(
        texts=["test"],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    print("✅ Cohere API key is valid!")
except Exception as e:
    print(f"❌ Cohere API key error: {e}")

# Test Pinecone connection
try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    print(f"✅ Pinecone API key is valid! Indexes: {pc.list_indexes().names()}")
except Exception as e:
    print(f"❌ Pinecone API key error: {e}")
