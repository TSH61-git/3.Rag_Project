import sys
sys.path.append('src')

from indexer import load_existing_index
from rag_workflow import RAGWorkflow

# Load index
print("Loading index...")
index = load_existing_index()

# Create workflow
workflow = RAGWorkflow(index=index)

# Check available methods
print("\nAvailable methods in workflow:")
methods = [m for m in dir(workflow) if not m.startswith('_') and 'draw' in m.lower() or 'diagram' in m.lower() or 'visual' in m.lower()]
print(methods)

print("\nAll public methods:")
all_methods = [m for m in dir(workflow) if not m.startswith('_') and callable(getattr(workflow, m))]
for method in all_methods:
    print(f"  - {method}")
