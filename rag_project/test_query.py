import sys
sys.path.append('src')

from indexer import load_existing_index
from query_engine import create_query_engine, query

# Load index
print("Loading index...")
index = load_existing_index()
query_engine = create_query_engine(index)
print("Index loaded successfully!")

# Test query
test_question = "What is the primary color in the design system?"
print(f"\nTesting with question: {test_question}")
response = query(query_engine, test_question)
print(f"\nResponse:\n{response}")
print(f"\nResponse type: {type(response)}")
print(f"\nResponse str: {str(response)}")
