from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.cohere import CohereEmbedding
import config
from pathlib import Path

def create_index(documents):
    """Create vector store index from documents"""
    
    # Initialize Cohere embeddings
    embed_model = CohereEmbedding(
        api_key=config.COHERE_API_KEY,
        model_name="embed-english-v3.0",
        input_type="search_document"
    )
    
    # Parse documents into nodes
    parser = SentenceSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    nodes = parser.get_nodes_from_documents(documents)
    
    print(f"Created {len(nodes)} nodes from documents")
    
    # Create index with local storage
    index = VectorStoreIndex(
        nodes=nodes,
        embed_model=embed_model,
        show_progress=True
    )
    
    # Save to disk
    storage_dir = Path(config.STORAGE_DIR)
    storage_dir.mkdir(exist_ok=True)
    index.storage_context.persist(persist_dir=str(storage_dir))
    
    print(f"Index saved to {storage_dir}")
    return index

def load_existing_index():
    """Load existing index from disk"""
    from llama_index.core import load_index_from_storage
    
    embed_model = CohereEmbedding(
        api_key=config.COHERE_API_KEY,
        model_name="embed-english-v3.0",
        input_type="search_query"
    )
    
    storage_dir = Path(config.STORAGE_DIR)
    storage_context = StorageContext.from_defaults(persist_dir=str(storage_dir))
    
    index = load_index_from_storage(
        storage_context=storage_context,
        embed_model=embed_model
    )
    
    return index
