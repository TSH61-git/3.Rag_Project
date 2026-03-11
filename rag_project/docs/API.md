# 📡 API Documentation

## מחלקות עיקריות

### 1. Data Loader

```python
def load_documents() -> List[Document]:
    """טוען מסמכים מכל התיקיות"""
```

**דוגמה:**
```python
from data_loader import load_documents
docs = load_documents()
```

### 2. Indexer

```python
def create_index(documents: List[Document]) -> VectorStoreIndex:
    """יוצר אינדקס חדש"""

def load_existing_index() -> VectorStoreIndex:
    """טוען אינדקס קיים"""
```

**דוגמה:**
```python
from indexer import create_index, load_existing_index
index = load_existing_index()
```

### 3. Workflow

```python
class SyncRAGWorkflow:
    def __init__(self, index: VectorStoreIndex, max_attempts: int = 2):
        pass
    
    def run(self, query: str) -> str:
        """מריץ workflow מלא"""
```

**דוגמה:**
```python
from sync_event_workflow_v2 import SyncRAGWorkflow
workflow = SyncRAGWorkflow(index=index, max_attempts=2)
response = workflow.run("What is the main color?")
```

### 4. Query Router

```python
class QueryRouter:
    def route(self, query: str) -> str:
        """מנתב שאילתה: semantic/structured"""
```

### 5. Query Classifier

```python
class QueryClassifier:
    def classify(self, query: str) -> Dict:
        """מסווג שאילתה"""
```

### 6. Data Extractor

```python
class DataExtractor:
    def extract(self, query: str, documents: List[Document]) -> Dict:
        """מחלץ נתונים מובנים"""
```

## Events

| Event | תיאור | Payload |
|-------|-------|---------|
| `input_validated` | קלט אומת | `{"query": str}` |
| `routing_complete` | ניתוב הושלם | `{"route": str}` |
| `nodes_retrieved` | מסמכים נשלפו | `{"count": int}` |
| `quality_checked` | בדיקת איכות | `{"confidence": float}` |
| `llm_complete` | LLM סיים | `{"response": str}` |
| `retry_triggered` | retry הופעל | `{"attempt": int}` |

## State Management

```python
@dataclass
class WorkflowState:
    query: str
    retrieved_nodes: List[NodeWithScore]
    confidence: float
    attempt: int
    route: str
    extracted_data: Optional[Dict]
```

## Error Handling

```python
class WorkflowError(Exception):
    pass

class ValidationError(WorkflowError):
    pass

class RetrievalError(WorkflowError):
    pass
```

## דוגמה מלאה

```python
import sys
sys.path.append('src')

from indexer import load_existing_index
from sync_event_workflow_v2 import SyncRAGWorkflow

index = load_existing_index()
workflow = SyncRAGWorkflow(index=index, max_attempts=2)
response = workflow.run("What are the main decisions?")
print(response)
```
