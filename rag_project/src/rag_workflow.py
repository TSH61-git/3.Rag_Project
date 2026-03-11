from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event,
    Context
)
from dataclasses import dataclass
from typing import List, Optional

# Custom Events
@dataclass
class InputValidatedEvent(Event):
    query: str

@dataclass
class NodesRetrievedEvent(Event):
    query: str
    nodes: List
    
@dataclass
class QualityCheckedEvent(Event):
    query: str
    nodes: List
    confidence_score: float
    is_good_quality: bool

@dataclass
class ResponseFormattedEvent(Event):
    response: str

# Workflow Class
class RAGWorkflow(Workflow):
    """RAG Workflow with @step decorators"""
    
    def __init__(self, index):
        super().__init__()
        self.index = index
    
    @step
    async def validate_input(self, ctx: Context, ev: StartEvent) -> InputValidatedEvent | StopEvent:
        """Step 1: Validate user input"""
        query = ev.get("query", "")
        
        print(f"[Step 1] Validating input: '{query}'")
        
        if not query or query.strip() == "":
            print(f"[Step 1] ❌ Input invalid: empty query")
            return StopEvent(result="Invalid input: Query is empty. Please enter a valid question.")
        
        if len(query) < 3:
            print(f"[Step 1] ❌ Input invalid: too short")
            return StopEvent(result="Invalid input: Query too short (minimum 3 characters).")
        
        print(f"[Step 1] ✅ Input valid")
        return InputValidatedEvent(query=query)
    
    @step
    async def retrieve_nodes(self, ctx: Context, ev: InputValidatedEvent) -> NodesRetrievedEvent | StopEvent:
        """Step 2: Retrieve relevant nodes from index"""
        query = ev.query
        
        print(f"[Step 2] Retrieving nodes for: '{query}'")
        
        try:
            retriever = self.index.as_retriever(similarity_top_k=3)
            nodes = retriever.retrieve(query)
            
            if not nodes:
                print(f"[Step 2] ❌ No nodes found")
                return StopEvent(result="No relevant information found. Try rephrasing your question.")
            
            print(f"[Step 2] ✅ Found {len(nodes)} nodes")
            return NodesRetrievedEvent(query=query, nodes=nodes)
            
        except Exception as e:
            print(f"[Step 2] ❌ Error: {e}")
            return StopEvent(result=f"An error occurred during retrieval: {str(e)}")
    
    @step
    async def check_quality(self, ctx: Context, ev: NodesRetrievedEvent) -> QualityCheckedEvent:
        """Step 3: Check quality of retrieved nodes"""
        nodes = ev.nodes
        
        print(f"[Step 3] Checking quality of {len(nodes)} nodes")
        
        # Calculate average score
        avg_score = sum(node.score for node in nodes) / len(nodes) if nodes else 0.0
        
        # Quality threshold
        QUALITY_THRESHOLD = 0.2
        is_good_quality = avg_score >= QUALITY_THRESHOLD
        
        if is_good_quality:
            print(f"[Step 3] ✅ Quality good (avg score: {avg_score:.2f})")
        else:
            print(f"[Step 3] ⚠️ Quality low (avg score: {avg_score:.2f})")
        
        return QualityCheckedEvent(
            query=ev.query,
            nodes=nodes,
            confidence_score=avg_score,
            is_good_quality=is_good_quality
        )
    
    @step
    async def format_response(self, ctx: Context, ev: QualityCheckedEvent) -> StopEvent:
        """Step 4: Format the final response"""
        print(f"[Step 4] Formatting response")
        
        nodes = ev.nodes
        confidence = ev.confidence_score
        
        # Build response
        response_parts = []
        response_parts.append(f"Found {len(nodes)} relevant sections (confidence: {confidence:.2f}):\n")
        
        for i, node in enumerate(nodes, 1):
            response_parts.append(f"\n--- Source {i} (Score: {node.score:.2f}) ---")
            response_parts.append(f"From: {node.metadata.get('tool', 'unknown')} - {node.metadata.get('file_name', 'unknown')}")
            response_parts.append(f"\n{node.text}\n")
        
        response = "\n".join(response_parts)
        
        print(f"[Step 4] ✅ Response ready (length: {len(response)})")
        
        return StopEvent(result=response)
