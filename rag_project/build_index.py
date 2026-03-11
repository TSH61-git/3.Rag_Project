import sys
sys.path.append('src')

from data_loader import load_documents
from indexer import create_index

def main():
    print("Starting index building process...")
    
    # Load documents
    print("\n1. Loading documents...")
    documents = load_documents()
    
    if not documents:
        print("No documents found. Please check your mock_docs directory.")
        return
    
    # Create index
    print("\n2. Creating vector index...")
    index = create_index(documents)
    
    print("\nIndex built successfully!")
    print("You can now run the chat interface with: python app.py")

if __name__ == "__main__":
    main()
