from llama_index.core import SimpleDirectoryReader
from pathlib import Path
import config

def load_documents():
    """Load all markdown documents from configured paths"""
    all_documents = []
    
    for tool_name, path in config.DOCS_PATHS.items():
        full_path = Path(path)
        if not full_path.exists():
            print(f"Warning: Path does not exist: {full_path}")
            continue
        
        try:
            reader = SimpleDirectoryReader(
                input_dir=str(full_path),
                required_exts=[".md"],
                recursive=True
            )
            documents = reader.load_data()
            
            for doc in documents:
                doc.metadata["tool"] = tool_name
                doc.metadata["source_path"] = str(doc.metadata.get("file_path", ""))
            
            all_documents.extend(documents)
            print(f"Loaded {len(documents)} documents from {tool_name}")
        except ValueError as e:
            print(f"Warning: Could not load from {tool_name}: {e}")
            continue
    
    print(f"Total documents loaded: {len(all_documents)}")
    return all_documents
