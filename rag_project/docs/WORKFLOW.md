# 🔄 Workflow Documentation

## סקירה כללית

המערכת משתמשת ב-Event-Driven Workflow עם 6 שלבים עיקריים.

## שלבי Workflow

### 1. Input Validation
**קובץ:** `src/sync_event_workflow_v2.py`

```python
def validate_input(self, query: str) -> Dict:
    """אימות קלט ואתחול state"""
    if not query or len(query.strip()) < 3:
        raise ValidationError("Query too short")
    
    return {
        "query": query,
        "state": WorkflowState(query=query)
    }
```

**בדיקות:**
- אורך מינימלי (3 תווים)
- קלט לא ריק
- תווים חוקיים

### 2. Query Routing
**קובץ:** `src/routing/query_router.py`

```python
def route(self, query: str) -> str:
    """ניתוב לפי סוג שאילתה"""
    keywords = {
        "structured": ["list", "show", "all", "רשום", "הצג"],
        "semantic": ["explain", "how", "why", "הסבר", "איך"]
    }
    
    for word in query.lower().split():
        if word in keywords["structured"]:
            return "structured"
    
    return "semantic"
```

**סוגי ניתוב:**
- **Semantic** - שאלות פתוחות
- **Structured** - רשימות ונתונים

### 3. Node Retrieval
**קובץ:** `src/sync_event_workflow_v2.py`

```python
def retrieve_nodes(self, query: str, top_k: int = 3) -> List[NodeWithScore]:
    """שליפת מסמכים רלוונטיים"""
    retriever = self.index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)
    return nodes
```

**פרמטרים:**
- `top_k=3` - ניסיון ראשון
- `top_k=5` - retry

### 4. Quality Check
**קובץ:** `src/sync_event_workflow_v2.py`

```python
def check_quality(self, nodes: List[NodeWithScore], attempt: int) -> str:
    """בדיקת איכות ותוצאות"""
    if not nodes:
        return "retry" if attempt < max_attempts else "stop"
    
    confidence = sum(node.score for node in nodes) / len(nodes)
    
    if confidence >= 0.3:
        return "continue"
    elif confidence >= 0.15:
        return "continue_with_warning"
    else:
        return "retry" if attempt < max_attempts else "stop"
```

**Thresholds:**
- `>= 0.3` - המשך
- `>= 0.15` - המשך עם אזהרה
- `< 0.15` - retry

### 5. LLM Synthesis
**קובץ:** `src/sync_event_workflow_v2.py`

```python
def synthesize(self, query: str, nodes: List[NodeWithScore]) -> str:
    """סינתזת תשובה עם LLM"""
    context = "\n\n".join([node.text for node in nodes])
    
    prompt = f"""
    Context: {context}
    
    Question: {query}
    
    Answer based on the context above.
    """
    
    response = self.llm.complete(prompt)
    return response.text
```

**מודלים:**
- Cohere: `command-r-plus-08-2024`
- Ollama: `llama3.2`

### 6. Response Formatting
**קובץ:** `src/sync_event_workflow_v2.py`

```python
def format_response(self, response: str, metadata: Dict) -> str:
    """עיצוב תשובה סופית"""
    formatted = f"{response}\n\n"
    
    if metadata.get("confidence") < 0.3:
        formatted += "⚠️ Low confidence - results may be incomplete\n"
    
    formatted += f"📊 Sources: {metadata['num_sources']}\n"
    formatted += f"🔄 Attempts: {metadata['attempts']}\n"
    
    return formatted
```

## זרימת Events

```
START
  ↓
[input_validated]
  ↓
[routing_complete] → route: semantic/structured
  ↓
[nodes_retrieved] → count: 3-5
  ↓
[quality_checked] → confidence: 0.0-1.0
  ↓
  ├─ High → [llm_synthesis_start]
  ├─ Low → [retry_triggered] → back to retrieve
  └─ Failed → [workflow_failed]
  ↓
[llm_complete]
  ↓
[response_formatted]
  ↓
END
```

## State Management

```python
@dataclass
class WorkflowState:
    query: str
    retrieved_nodes: List[NodeWithScore] = field(default_factory=list)
    confidence: float = 0.0
    attempt: int = 1
    route: str = "semantic"
    extracted_data: Optional[Dict] = None
    metadata: Dict = field(default_factory=dict)
```

## Retry Logic

```python
def handle_retry(self, state: WorkflowState) -> WorkflowState:
    """טיפול ב-retry"""
    state.attempt += 1
    
    if state.attempt > self.max_attempts:
        raise MaxAttemptsError("Max retries reached")
    
    # הגדל top_k
    top_k = 3 + (state.attempt * 2)
    
    # נסה שוב
    state.retrieved_nodes = self.retrieve_nodes(state.query, top_k)
    
    return state
```

## Error Handling

```python
try:
    response = workflow.run(query)
except ValidationError as e:
    print(f"Invalid input: {e}")
except RetrievalError as e:
    print(f"Retrieval failed: {e}")
except LLMError as e:
    print(f"LLM failed: {e}")
except MaxAttemptsError as e:
    print(f"Max retries: {e}")
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| Avg Query Time | 1-3s |
| Retrieval Time | 0.2-0.5s |
| LLM Time | 0.8-2.5s |
| Success Rate | 85-95% |
| Retry Rate | 10-15% |

## Optimization Tips

### 1. הגדלת דיוק
```python
CHUNK_SIZE = 128
TOP_K = 10
HIGH_CONFIDENCE = 0.5
```

### 2. הגדלת מהירות
```python
CHUNK_SIZE = 512
TOP_K = 3
MAX_ATTEMPTS = 1
```

### 3. איזון
```python
CHUNK_SIZE = 256
TOP_K = 5
MAX_ATTEMPTS = 2
```

## Debugging

### הפעלת Verbose Mode
```python
workflow = SyncRAGWorkflow(index=index, verbose=True)
```

### לוגים
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### בדיקת State
```python
state = workflow.get_state()
print(f"Attempt: {state.attempt}")
print(f"Confidence: {state.confidence}")
print(f"Route: {state.route}")
```
