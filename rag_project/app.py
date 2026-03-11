import sys
sys.path.append('src')

import gradio as gr
from indexer import load_existing_index
from sync_event_workflow_v2 import SyncRAGWorkflow

# Load index
print("Loading index...")
index = load_existing_index()
print("Index loaded successfully!")

# Create workflow
workflow = SyncRAGWorkflow(index=index, max_attempts=2)
print("\n" + "="*60)
print("RAG Workflow - Event-Driven with Routing (Stage C)")
print("="*60)
print("\nWorkflow Steps:")
print("  1. Input Validation")
print("  2. Query Routing (Semantic vs Structured) [NEW]")
print("  3a. Structured Query (if needed) [NEW]")
print("  3b. Node Retrieval (semantic path)")
print("  4. Quality Check")
print("  5. LLM Synthesis")
print("  6. Response Formatting")
print("\nFeatures:")
print("  - Intelligent routing (semantic vs structured)")
print("  - Structured data queries (lists, filters, latest)")
print("  - Event-driven with state management")
print("  - Automatic retry with more context")
print("  - Cohere LLM (command-r-plus-08-2024)")
print("="*60 + "\n")

def chat(message, history):
    """Handle chat messages using synchronous event-driven workflow"""
    try:
        response = workflow.run(query=message)
        return response
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"An unexpected error occurred: {str(e)}"

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat,
    title="🔍 RAG Documentation Assistant",
    description="Ask questions about your project documentation from Cursor and Claude Code",
    examples=[
        "What is the primary color in the design system?",
        "List all technical decisions",
        "Show me all critical warnings",
        "What are the RTL rules for the interface?",
        "What database changes were made recently?",
        "How do I install the system?",
        "What technical decisions were made about authentication?"
    ]
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
