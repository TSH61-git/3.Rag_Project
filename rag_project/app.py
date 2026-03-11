import sys
sys.path.append('src')

import gradio as gr
from indexer import load_existing_index
from sync_event_workflow import SyncRAGWorkflow

# Load index
print("Loading index...")
index = load_existing_index()
print("Index loaded successfully!")

# Create workflow
workflow = SyncRAGWorkflow(index=index, max_attempts=2)
print("\n" + "="*60)
print("RAG Workflow - Synchronous Event-Driven Architecture")
print("="*60)
print("\nWorkflow Steps:")
print("  1. Input Validation - validates query and initializes state")
print("  2. Node Retrieval - fetches relevant documents (with retry)")
print("  3. Quality Check - evaluates confidence and routes accordingly")
print("  4. LLM Synthesis - generates natural language response")
print("  5. Response Formatting - adds metadata and finalizes")
print("\nFeatures:")
print("  ✅ Event-driven routing based on quality")
print("  ✅ State management for attempts and history")
print("  ✅ Automatic retry with more context if needed")
print("  ✅ Multiple validations at each step")
print("  ✅ Cohere LLM (command-r-plus-08-2024)")
print("  ✅ No async complexity - works perfectly with Gradio")
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
        "Which languages are supported for translation?",
        "What database changes were made recently?",
        "What are the RTL rules for the interface?",
        "What are the sensitive areas in the codebase?",
        "How do I install the system?",
        "What technical decisions were made about authentication?"
    ]
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
