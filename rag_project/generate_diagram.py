import sys
sys.path.append('src')

from indexer import load_existing_index
from rag_workflow import RAGWorkflow

# Load index
print("Loading index...")
index = load_existing_index()
print("Index loaded successfully!")

# Create workflow
workflow = RAGWorkflow(index=index)
print("Workflow created!")

# Draw the workflow diagram
print("\nGenerating workflow diagram...")
try:
    # Try the correct method name
    workflow.draw_all_possible_flows(filename="workflow_diagram.html")
except AttributeError:
    # Fallback to alternative method
    try:
        from llama_index.core.workflow import draw_all_possible_flows
        draw_all_possible_flows(workflow, filename="workflow_diagram.html")
    except Exception as e:
        print(f"Method 1 failed: {e}")
        # Manual visualization
        html = workflow.get_diagram()
        with open("workflow_diagram.html", "w", encoding="utf-8") as f:
            f.write(html)

print("✅ Diagram saved to: workflow_diagram.html")
print("\nOpen the file in your browser to see the workflow visualization!")
