import sys
sys.path.append('src')

import gradio as gr
from indexer import load_existing_index
from simple_rag import SimpleRAGPipeline

# Load index
print("Loading index...")
index = load_existing_index()
print("Index loaded successfully!")

# Create pipeline
pipeline = SimpleRAGPipeline(index=index)
print("RAG Pipeline initialized with 5 steps:")
print("  1. Input Validation")
print("  2. Node Retrieval")
print("  3. Quality Check")
print("  4. LLM Synthesis (Cohere)")
print("  5. Response Formatting")
print()

def chat(message, history):
    """Handle chat messages using simple RAG pipeline"""
    try:
        response = pipeline.query(message)
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
