from llama_index.core.postprocessor import SimilarityPostprocessor
import config

def create_query_engine(index, use_ollama=True):
    """Create query engine with LLM"""
    
    if use_ollama:
        try:
            from llama_index.llms.ollama import Ollama
            llm = Ollama(model="llama3.2", request_timeout=120.0)
            print("Using Ollama (local LLM)")
        except Exception as e:
            print(f"Ollama not available: {e}")
            print("Falling back to retrieval-only mode")
            return None
    else:
        try:
            from llama_index.llms.cohere import Cohere
            llm = Cohere(
                api_key=config.COHERE_API_KEY,
                model="command"
            )
            print("Using Cohere LLM")
        except Exception as e:
            print(f"Cohere not available: {e}")
            return None
    
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=3,
        node_postprocessors=[
            SimilarityPostprocessor(similarity_cutoff=0.5)
        ],
        response_mode="compact"
    )
    
    return query_engine

def query(index_or_engine, question):
    """Execute query and return response"""
    
    # Check if we have a query engine or just an index
    if hasattr(index_or_engine, 'query'):
        # It's a query engine - use LLM
        try:
            response = index_or_engine.query(question)
            return str(response)
        except Exception as e:
            print(f"LLM query failed: {e}")
            # Fallback to retrieval
            pass
    
    # Fallback: retrieval-only mode
    index = index_or_engine if not hasattr(index_or_engine, 'query') else index_or_engine._index
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(question)
    
    if not nodes:
        return "No relevant information found."
    
    # Build response from retrieved nodes
    response_parts = []
    response_parts.append(f"Found {len(nodes)} relevant sections:\n")
    
    for i, node in enumerate(nodes, 1):
        response_parts.append(f"\n--- Source {i} (Score: {node.score:.2f}) ---")
        response_parts.append(f"From: {node.metadata.get('tool', 'unknown')} - {node.metadata.get('file_name', 'unknown')}")
        response_parts.append(f"\n{node.text}\n")
    
    return "\n".join(response_parts)
