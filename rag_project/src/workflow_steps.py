from workflow_models import QueryState, Event, EventType

class WorkflowSteps:
    """כל השלבים בתהליך השאילתה"""
    
    @staticmethod
    def validate_input(state: QueryState) -> Event:
        """שלב 1: בדיקת תקינות הקלט"""
        print(f"[Step 1] Validating input: '{state.query}'")
        
        if not state.query or state.query.strip() == "":
            return Event(
                type=EventType.INPUT_INVALID,
                message="Query is empty"
            )
        
        if len(state.query) < 3:
            return Event(
                type=EventType.INPUT_INVALID,
                message="Query too short (minimum 3 characters)"
            )
        
        print(f"[Step 1] ✅ Input valid")
        return Event(
            type=EventType.INPUT_VALID,
            message="Input is valid"
        )
    
    @staticmethod
    def retrieve_nodes(state: QueryState, index) -> Event:
        """שלב 2: חיפוש במסמכים"""
        print(f"[Step 2] Retrieving nodes for: '{state.query}'")
        
        try:
            retriever = index.as_retriever(similarity_top_k=3)
            nodes = retriever.retrieve(state.query)
            
            state.nodes = nodes
            
            if not nodes:
                print(f"[Step 2] ❌ No nodes found")
                return Event(
                    type=EventType.NO_NODES_FOUND,
                    message="No relevant documents found"
                )
            
            print(f"[Step 2] ✅ Found {len(nodes)} nodes")
            return Event(
                type=EventType.NODES_FOUND,
                message=f"Found {len(nodes)} nodes",
                data={"count": len(nodes)}
            )
            
        except Exception as e:
            print(f"[Step 2] ❌ Error: {e}")
            state.error = str(e)
            return Event(
                type=EventType.ERROR,
                message=f"Retrieval error: {e}"
            )
    
    @staticmethod
    def check_quality(state: QueryState) -> Event:
        """שלב 3: בדיקת איכות התוצאות"""
        print(f"[Step 3] Checking quality of {len(state.nodes)} nodes")
        
        if not state.has_nodes():
            return Event(
                type=EventType.NO_NODES_FOUND,
                message="No nodes to check"
            )
        
        avg_score = state.get_avg_score()
        state.confidence_score = avg_score
        
        # סף איכות: 0.2 ומעלה = טוב
        QUALITY_THRESHOLD = 0.2
        
        if avg_score >= QUALITY_THRESHOLD:
            print(f"[Step 3] ✅ Quality good (avg score: {avg_score:.2f})")
            return Event(
                type=EventType.QUALITY_GOOD,
                message=f"Good quality results (score: {avg_score:.2f})",
                data={"score": avg_score}
            )
        else:
            print(f"[Step 3] ⚠️ Quality low (avg score: {avg_score:.2f})")
            return Event(
                type=EventType.QUALITY_LOW,
                message=f"Low quality results (score: {avg_score:.2f})",
                data={"score": avg_score}
            )
    
    @staticmethod
    def format_response(state: QueryState) -> Event:
        """שלב 4: עיצוב התשובה"""
        print(f"[Step 4] Formatting response")
        
        if not state.has_nodes():
            state.response = "No relevant information found."
            return Event(
                type=EventType.RESPONSE_READY,
                message="Empty response ready"
            )
        
        # בניית התשובה
        response_parts = []
        response_parts.append(f"Found {len(state.nodes)} relevant sections (confidence: {state.confidence_score:.2f}):\n")
        
        for i, node in enumerate(state.nodes, 1):
            response_parts.append(f"\n--- Source {i} (Score: {node.score:.2f}) ---")
            response_parts.append(f"From: {node.metadata.get('tool', 'unknown')} - {node.metadata.get('file_name', 'unknown')}")
            response_parts.append(f"\n{node.text}\n")
        
        state.response = "\n".join(response_parts)
        
        print(f"[Step 4] ✅ Response ready (length: {len(state.response)})")
        return Event(
            type=EventType.RESPONSE_READY,
            message="Response formatted successfully"
        )
