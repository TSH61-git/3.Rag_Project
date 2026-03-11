"""Simple synchronous RAG pipeline"""
import config

class SimpleRAGPipeline:
    """Simple RAG pipeline without async complexity"""
    
    def __init__(self, index):
        self.index = index
    
    def query(self, question: str) -> str:
        """Process query through RAG pipeline"""
        
        # Step 1: Validate input
        print(f"[Step 1] Validating input: '{question}'")
        if not question or question.strip() == "":
            return "Invalid input: Query is empty. Please enter a valid question."
        if len(question) < 3:
            return "Invalid input: Query too short (minimum 3 characters)."
        print(f"[Step 1] ✅ Input valid")
        
        # Step 2: Retrieve nodes
        print(f"[Step 2] Retrieving nodes for: '{question}'")
        try:
            retriever = self.index.as_retriever(similarity_top_k=3)
            nodes = retriever.retrieve(question)
            
            if not nodes:
                print(f"[Step 2] ❌ No nodes found")
                return "No relevant information found. Try rephrasing your question."
            
            print(f"[Step 2] ✅ Found {len(nodes)} nodes")
        except Exception as e:
            print(f"[Step 2] ❌ Error: {e}")
            return f"An error occurred during retrieval: {str(e)}"
        
        # Step 3: Check quality
        print(f"[Step 3] Checking quality of {len(nodes)} nodes")
        avg_score = sum(node.score for node in nodes) / len(nodes) if nodes else 0.0
        QUALITY_THRESHOLD = 0.2
        is_good_quality = avg_score >= QUALITY_THRESHOLD
        
        if is_good_quality:
            print(f"[Step 3] ✅ Quality good (avg score: {avg_score:.2f})")
        else:
            print(f"[Step 3] ⚠️ Quality low (avg score: {avg_score:.2f})")
        
        # Step 4: Synthesize response with LLM
        print(f"[Step 4] Synthesizing response with LLM")
        
        # Build context from nodes
        context_parts = []
        for i, node in enumerate(nodes, 1):
            tool = node.metadata.get('tool', 'unknown')
            file_name = node.metadata.get('file_name', 'unknown')
            context_parts.append(f"[Source {i} - {tool}/{file_name}]\n{node.text}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        prompt = f"""Based on the following documentation excerpts, answer the user's question.

Question: {question}

Documentation:
{context}

Provide a clear, concise answer based on the documentation above. If the documentation doesn't contain enough information, say so."""
        
        # Call LLM using Chat API
        try:
            from cohere import Client
            client = Client(api_key=config.COHERE_API_KEY)
            
            # Try newest models first
            models_to_try = ["command-r-plus-08-2024", "command-r-08-2024", "command-r7b-12-2024"]
            
            answer = None
            for model in models_to_try:
                try:
                    print(f"[Step 4] Trying model: {model}...")
                    response = client.chat(
                        model=model,
                        message=prompt,
                        temperature=0.3
                    )
                    answer = response.text
                    print(f"[Step 4] ✅ LLM response generated with {model} (length: {len(answer)})")
                    break
                except Exception as model_error:
                    print(f"[Step 4] ⚠️ Model {model} failed: {str(model_error)[:100]}")
                    continue
            
            if answer is None:
                raise Exception("All models failed")
        except Exception as e:
            print(f"[Step 4] ❌ All LLM attempts failed: {str(e)[:200]}")
            # Fallback to simple concatenation
            answer = f"Found {len(nodes)} relevant sections:\n\n" + context
        
        # Step 5: Format response
        print(f"[Step 5] ✅ Response ready")
        return answer
