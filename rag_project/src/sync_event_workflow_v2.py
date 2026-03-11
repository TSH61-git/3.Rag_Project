"""Synchronous Event-Driven RAG Workflow with Routing"""
from dataclasses import dataclass
from typing import List, Optional, Union
import config
from routing.query_router import QueryRouter
from extraction.structured_query import StructuredQueryEngine

# Events
@dataclass
class InputValidatedEvent:
    query: str

@dataclass
class QueryRoutedEvent:
    query: str
    engine: str  # "semantic" or "structured"
    classification: dict
    structured_results: Optional[List] = None

@dataclass
class NodesRetrievedEvent:
    query: str
    nodes: List
    attempt: int = 1

@dataclass
class QualityCheckedEvent:
    query: str
    nodes: List
    confidence_score: float
    is_good_quality: bool
    attempt: int

@dataclass
class NeedMoreContextEvent:
    query: str
    previous_nodes: List
    attempt: int

@dataclass
class ResponseSynthesizedEvent:
    response: str
    confidence_score: float

@dataclass
class StopEvent:
    result: str

# Workflow State
class WorkflowState:
    def __init__(self):
        self.total_attempts = 0
        self.all_nodes_seen = []
        self.used_structured = False
        self.structured_category = None

# Synchronous Event-Driven Workflow
class SyncRAGWorkflow:
    """Event-Driven RAG with Routing"""
    
    def __init__(self, index, max_attempts=2):
        self.index = index
        self.max_attempts = max_attempts
        self.router = QueryRouter()
        self.structured_engine = StructuredQueryEngine()
    
    def run(self, query: str) -> str:
        """Run the workflow synchronously"""
        state = WorkflowState()
        
        # Step 1: Validate Input
        event = self.validate_input(query, state)
        if isinstance(event, StopEvent):
            return event.result
        
        # Step 2: Route Query (NEW!)
        event = self.route_query(event, state)
        if isinstance(event, StopEvent):
            return event.result
        
        # Check if we used structured engine
        if state.used_structured:
            # Skip to synthesis with structured results
            event = self.synthesize_structured_response(event, state)
            if isinstance(event, StopEvent):
                return event.result
            
            # Format and return
            event = self.format_response(event, state)
            return event.result
        
        # Continue with semantic search (Steps 3-6)
        # Step 3: Retrieve Nodes (with potential retry loop)
        while True:
            event = self.retrieve_nodes(event, state)
            if isinstance(event, StopEvent):
                return event.result
            
            # Step 4: Check Quality
            event = self.check_quality(event, state)
            if isinstance(event, StopEvent):
                return event.result
            elif isinstance(event, NeedMoreContextEvent):
                # Retry: go back to retrieve with more context
                continue
            else:
                # Quality is good enough, continue
                break
        
        # Step 5: Synthesize Response
        event = self.synthesize_response(event, state)
        if isinstance(event, StopEvent):
            return event.result
        
        # Step 6: Format Response
        event = self.format_response(event, state)
        return event.result
    
    def validate_input(self, query: str, state: WorkflowState) -> Union[InputValidatedEvent, StopEvent]:
        """Step 1: Validate user input"""
        print(f"[Step 1] Validating input: '{query}'")
        
        # Initialize state
        state.total_attempts = 0
        state.all_nodes_seen = []
        
        # Validations
        if not query or query.strip() == "":
            print(f"[Step 1] ❌ Input invalid: empty query")
            return StopEvent(result="Invalid input: Query is empty. Please enter a valid question.")
        
        if len(query) < 3:
            print(f"[Step 1] ❌ Input invalid: too short")
            return StopEvent(result="Invalid input: Query too short (minimum 3 characters).")
        
        if len(query) > 500:
            print(f"[Step 1] ⚠️ Input warning: very long query, truncating")
            query = query[:500]
        
        print(f"[Step 1] ✅ Input valid")
        return InputValidatedEvent(query=query)
    
    def route_query(self, event: InputValidatedEvent, state: WorkflowState) -> Union[QueryRoutedEvent, StopEvent]:
        """Step 2: Route query to appropriate engine"""
        query = event.query
        
        print(f"[Step 2] Routing query")
        
        try:
            routing_result = self.router.route(query)
            
            engine = routing_result["engine"]
            classification = routing_result["classification"]
            structured_results = routing_result.get("structured_results")
            
            if engine == "structured":
                state.used_structured = True
                state.structured_category = classification.get("category")
                
                if not structured_results:
                    print(f"[Step 2] ❌ No structured results found")
                    return StopEvent(result="No matching items found in the structured data.")
                
                print(f"[Step 2] ✅ Using structured engine with {len(structured_results)} results")
            else:
                print(f"[Step 2] ✅ Using semantic engine")
            
            return QueryRoutedEvent(
                query=query,
                engine=engine,
                classification=classification,
                structured_results=structured_results
            )
            
        except Exception as e:
            print(f"[Step 2] ⚠️ Routing error: {e}, falling back to semantic")
            return QueryRoutedEvent(
                query=query,
                engine="semantic",
                classification={},
                structured_results=None
            )
    
    def synthesize_structured_response(self, event: QueryRoutedEvent, state: WorkflowState) -> Union[ResponseSynthesizedEvent, StopEvent]:
        """Step 3b: Synthesize response from structured data"""
        print(f"[Step 3b] Synthesizing response from structured data")
        
        query = event.query
        results = event.structured_results
        category = state.structured_category
        
        # Format structured results
        formatted_results = self.structured_engine.format_results(results, category)
        
        # Use LLM to create natural response
        prompt = f"""Based on the following structured data, provide a clear and natural answer to the user's question.

Question: {query}

Structured Data:
{formatted_results}

Provide a well-formatted, natural language response. If the data is a list, present it clearly. Include relevant details from the structured data."""
        
        try:
            from cohere import Client
            client = Client(api_key=config.COHERE_API_KEY)
            
            response = client.chat(
                model="command-r-plus-08-2024",
                message=prompt,
                temperature=0.3
            )
            answer = response.text
            print(f"[Step 3b] ✅ LLM response generated (length: {len(answer)})")
            
            return ResponseSynthesizedEvent(response=answer, confidence_score=1.0)
            
        except Exception as e:
            print(f"[Step 3b] ⚠️ LLM error: {e}, returning formatted results")
            return ResponseSynthesizedEvent(response=formatted_results, confidence_score=1.0)
    
    def retrieve_nodes(self, event: Union[QueryRoutedEvent, NeedMoreContextEvent], state: WorkflowState) -> Union[NodesRetrievedEvent, StopEvent]:
        """Step 3: Retrieve relevant nodes (semantic path)"""
        
        # Handle both event types
        if isinstance(event, QueryRoutedEvent):
            query = event.query
            attempt = 1
            top_k = 3
        else:  # NeedMoreContextEvent
            query = event.query
            attempt = event.attempt
            top_k = 5
            print(f"[Step 3] Retry attempt {attempt} - fetching more nodes (top_k={top_k})")
        
        print(f"[Step 3] Retrieving nodes for: '{query}' (attempt {attempt})")
        
        # Update state
        state.total_attempts = attempt
        
        try:
            retriever = self.index.as_retriever(similarity_top_k=top_k)
            nodes = retriever.retrieve(query)
            
            # Validation: no results
            if not nodes:
                print(f"[Step 3] ❌ No nodes found")
                return StopEvent(result="No relevant information found. Try rephrasing your question.")
            
            # Validation: check content
            valid_nodes = [n for n in nodes if n.text and len(n.text.strip()) > 10]
            if not valid_nodes:
                print(f"[Step 3] ❌ No valid content in nodes")
                return StopEvent(result="Found documents but they contain no useful content.")
            
            print(f"[Step 3] ✅ Found {len(valid_nodes)} valid nodes")
            
            # Store in state
            state.all_nodes_seen.extend(valid_nodes)
            
            return NodesRetrievedEvent(query=query, nodes=valid_nodes, attempt=attempt)
            
        except Exception as e:
            print(f"[Step 3] ❌ Error: {e}")
            return StopEvent(result=f"An error occurred during retrieval: {str(e)}")
    
    def check_quality(self, event: NodesRetrievedEvent, state: WorkflowState) -> Union[QualityCheckedEvent, NeedMoreContextEvent, StopEvent]:
        """Step 4: Check quality and route (semantic path)"""
        nodes = event.nodes
        query = event.query
        attempt = event.attempt
        
        print(f"[Step 4] Checking quality of {len(nodes)} nodes")
        
        # Calculate confidence
        avg_score = sum(node.score for node in nodes) / len(nodes) if nodes else 0.0
        
        # Thresholds
        GOOD_THRESHOLD = 0.25
        MIN_THRESHOLD = 0.10
        
        # Routing logic
        if avg_score >= GOOD_THRESHOLD:
            print(f"[Step 4] ✅ Quality good (avg score: {avg_score:.2f})")
            return QualityCheckedEvent(
                query=query,
                nodes=nodes,
                confidence_score=avg_score,
                is_good_quality=True,
                attempt=attempt
            )
        
        elif avg_score >= MIN_THRESHOLD:
            print(f"[Step 4] ⚠️ Quality acceptable (avg score: {avg_score:.2f})")
            return QualityCheckedEvent(
                query=query,
                nodes=nodes,
                confidence_score=avg_score,
                is_good_quality=False,
                attempt=attempt
            )
        
        else:
            # Very low quality - retry if possible
            if attempt < self.max_attempts:
                print(f"[Step 4] ⚠️ Quality too low (avg score: {avg_score:.2f}) - requesting more context")
                return NeedMoreContextEvent(
                    query=query,
                    previous_nodes=nodes,
                    attempt=attempt + 1
                )
            else:
                print(f"[Step 4] ❌ Quality too low after {attempt} attempts")
                return StopEvent(result=f"Could not find relevant information after {attempt} attempts. The documentation may not contain information about this topic.")
    
    def synthesize_response(self, event: QualityCheckedEvent, state: WorkflowState) -> Union[ResponseSynthesizedEvent, StopEvent]:
        """Step 5: Synthesize with LLM (semantic path)"""
        print(f"[Step 5] Synthesizing response with LLM")
        
        query = event.query
        nodes = event.nodes
        confidence = event.confidence_score
        
        # Build context
        context_parts = []
        for i, node in enumerate(nodes, 1):
            tool = node.metadata.get('tool', 'unknown')
            file_name = node.metadata.get('file_name', 'unknown')
            score = node.score
            context_parts.append(f"[Source {i} - {tool}/{file_name} - Score: {score:.2f}]\n{node.text}")
        
        context = "\n\n".join(context_parts)
        
        # Prompt with confidence awareness
        if event.is_good_quality:
            confidence_note = "The sources are highly relevant."
        else:
            confidence_note = "The sources have moderate relevance. If they don't fully answer the question, please indicate what information is missing."
        
        prompt = f"""Based on the following documentation excerpts, answer the user's question.

{confidence_note}

Question: {query}

Documentation:
{context}

Provide a clear, concise answer based on the documentation above. If the documentation doesn't contain enough information, say so."""
        
        # Call LLM
        try:
            from cohere import Client
            client = Client(api_key=config.COHERE_API_KEY)
            
            models_to_try = ["command-r-plus-08-2024", "command-r-08-2024", "command-r7b-12-2024"]
            
            answer = None
            for model in models_to_try:
                try:
                    print(f"[Step 5] Trying model: {model}...")
                    response = client.chat(
                        model=model,
                        message=prompt,
                        temperature=0.3
                    )
                    answer = response.text
                    print(f"[Step 5] ✅ LLM response generated with {model} (length: {len(answer)})")
                    break
                except Exception as model_error:
                    print(f"[Step 5] ⚠️ Model {model} failed: {str(model_error)[:100]}")
                    continue
            
            if answer is None:
                raise Exception("All models failed")
            
            return ResponseSynthesizedEvent(response=answer, confidence_score=confidence)
            
        except Exception as e:
            print(f"[Step 5] ❌ LLM error: {str(e)[:200]}")
            fallback = f"Found {len(nodes)} relevant sections (confidence: {confidence:.2f}):\n\n" + context
            return ResponseSynthesizedEvent(response=fallback, confidence_score=confidence)
    
    def format_response(self, event: ResponseSynthesizedEvent, state: WorkflowState) -> StopEvent:
        """Step 6: Format final response"""
        print(f"[Step 6] Formatting final response")
        
        response = event.response
        confidence = event.confidence_score
        total_attempts = state.total_attempts
        
        # Add metadata
        if total_attempts > 1:
            response += f"\n\n---\n*Note: This answer was generated after {total_attempts} retrieval attempts.*"
        
        if confidence < 0.3 and not state.used_structured:
            response += f"\n*Confidence: {confidence:.2f} - The answer may not be fully accurate.*"
        
        print(f"[Step 6] ✅ Response ready (attempts: {total_attempts}, confidence: {confidence:.2f})")
        
        return StopEvent(result=response)
