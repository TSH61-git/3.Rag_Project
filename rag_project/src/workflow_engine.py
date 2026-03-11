from workflow_models import QueryState, Event, EventType
from workflow_steps import WorkflowSteps

class WorkflowEngine:
    """המנוע שמריץ את כל התהליך"""
    
    def __init__(self, index):
        self.index = index
        self.steps = WorkflowSteps()
    
    def execute(self, query: str) -> str:
        """מריץ את כל התהליך מתחילה לסוף"""
        print(f"\n{'='*60}")
        print(f"🚀 Starting workflow for query: '{query}'")
        print(f"{'='*60}\n")
        
        # יצירת State ריק
        state = QueryState(query=query)
        
        # שלב 1: Validate Input
        event = self.steps.validate_input(state)
        if event.type == EventType.INPUT_INVALID:
            return self._handle_invalid_input(event)
        
        # שלב 2: Retrieve Nodes
        event = self.steps.retrieve_nodes(state, self.index)
        if event.type == EventType.ERROR:
            return self._handle_error(state, event)
        if event.type == EventType.NO_NODES_FOUND:
            return self._handle_no_results(event)
        
        # שלב 3: Check Quality
        event = self.steps.check_quality(state)
        if event.type == EventType.QUALITY_LOW:
            # אפשר להוסיף לוגיקה מיוחדת לאיכות נמוכה
            print("⚠️ Low quality detected, but continuing...")
        
        # שלב 4: Format Response
        event = self.steps.format_response(state)
        
        print(f"\n{'='*60}")
        print(f"✅ Workflow completed successfully")
        print(f"{'='*60}\n")
        
        return state.response
    
    def _handle_invalid_input(self, event: Event) -> str:
        """טיפול בקלט לא תקין"""
        print(f"❌ Invalid input: {event.message}")
        return f"Invalid input: {event.message}. Please enter a valid question."
    
    def _handle_no_results(self, event: Event) -> str:
        """טיפול במצב של אין תוצאות"""
        print(f"❌ No results: {event.message}")
        return "No relevant information found. Try rephrasing your question or asking about a different topic."
    
    def _handle_error(self, state: QueryState, event: Event) -> str:
        """טיפול בשגיאות"""
        print(f"❌ Error occurred: {event.message}")
        return f"An error occurred: {state.error}"
