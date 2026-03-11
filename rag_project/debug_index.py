import sys
sys.path.append('src')

from indexer import load_existing_index

# Load index
print("Loading index...")
index = load_existing_index()
print("Index loaded successfully!")

# Check index content
print(f"\nIndex type: {type(index)}")
print(f"\nTrying to retrieve nodes...")

# Get retriever
retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve("primary color")

print(f"\nFound {len(nodes)} nodes")
for i, node in enumerate(nodes):
    print(f"\n--- Node {i+1} ---")
    print(f"Score: {node.score}")
    print(f"Text preview: {node.text[:200]}...")
    print(f"Metadata: {node.metadata}")
