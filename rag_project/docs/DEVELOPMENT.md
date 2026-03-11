# 🛠️ מדריך פיתוח

## הגדרת סביבת פיתוח

### 1. Clone והתקנה
```bash
cd rag_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # כלי פיתוח
```

### 2. Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

## מבנה הפרויקט

```
rag_project/
├── src/                    # קוד מקור
│   ├── classification/     # סיווג שאילתות
│   ├── extraction/         # חילוץ נתונים
│   ├── routing/            # ניתוב
│   ├── utils/              # כלי עזר
│   ├── config.py           # הגדרות
│   ├── data_loader.py      # טעינת מסמכים
│   ├── indexer.py          # אינדוקס
│   └── sync_event_workflow_v2.py  # Workflow
├── scripts/                # סקריפטים
│   ├── doc_monitor.py      # ניטור תיעוד
│   └── extract_data.py     # חילוץ נתונים
├── docs/                   # תיעוד
├── tests/                  # בדיקות
├── mock_docs/              # מסמכים לדוגמה
└── data/                   # נתונים ואחסון
```

## הוספת תכונה חדשה

### 1. צור ענף חדש
```bash
git checkout -b feature/my-new-feature
```

### 2. כתוב קוד
```python
# src/my_module.py
class MyNewFeature:
    def __init__(self):
        pass
    
    def process(self, data):
        """תיאור הפונקציה"""
        return processed_data
```

### 3. כתוב בדיקות
```python
# tests/test_my_module.py
import pytest
from src.my_module import MyNewFeature

def test_my_feature():
    feature = MyNewFeature()
    result = feature.process("test")
    assert result == "expected"
```

### 4. הרץ בדיקות
```bash
pytest tests/
```

### 5. עדכן תיעוד
```bash
# docs/MY_FEATURE.md
# התכונה החדשה שלי
...
```

## קונבנציות קוד

### Python Style Guide
- PEP 8
- Type hints
- Docstrings

```python
def my_function(param: str, count: int = 5) -> List[str]:
    """
    תיאור הפונקציה
    
    Args:
        param: תיאור פרמטר
        count: מספר פריטים
        
    Returns:
        רשימת תוצאות
    """
    return ["result"] * count
```

### Naming Conventions
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_CASE`
- Private: `_leading_underscore`

### Imports
```python
# Standard library
import os
import sys

# Third party
from llama_index.core import VectorStoreIndex

# Local
from src.config import CHUNK_SIZE
```

## בדיקות (Testing)

### Unit Tests
```python
# tests/unit/test_data_loader.py
def test_load_documents():
    docs = load_documents()
    assert len(docs) > 0
    assert all(hasattr(doc, 'text') for doc in docs)
```

### Integration Tests
```python
# tests/integration/test_workflow.py
def test_full_workflow():
    index = load_existing_index()
    workflow = SyncRAGWorkflow(index=index)
    response = workflow.run("test query")
    assert response is not None
```

### הרצת בדיקות
```bash
# כל הבדיקות
pytest

# בדיקה ספציפית
pytest tests/test_my_module.py

# עם coverage
pytest --cov=src tests/
```

## Debugging

### VS Code Launch Config
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

## Performance Profiling

### cProfile
```bash
python -m cProfile -o output.prof app.py
```

### Memory Profiling
```bash
pip install memory_profiler
python -m memory_profiler app.py
```

## Documentation

### עדכון תיעוד אוטומטי
```bash
python scripts/doc_monitor.py
```

### יצירת תיעוד API
```bash
pip install pdoc3
pdoc --html --output-dir docs/api src/
```

## CI/CD

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest
```

## Release Process

### 1. עדכן גרסה
```python
# src/__version__.py
__version__ = "1.2.0"
```

### 2. עדכן CHANGELOG
```markdown
## [1.2.0] - 2024-01-15
### Added
- תכונה חדשה X
### Fixed
- תיקון באג Y
```

### 3. צור Tag
```bash
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

## Best Practices

### 1. Code Review
- בדוק קוד לפני merge
- השתמש ב-pull requests
- כתוב הערות מועילות

### 2. Documentation
- עדכן תיעוד עם כל שינוי
- כתוב docstrings
- הוסף דוגמאות

### 3. Testing
- כתוב בדיקות לכל תכונה
- שמור על coverage גבוה (>80%)
- בדוק edge cases

### 4. Security
- אל תשמור מפתחות בקוד
- השתמש ב-.env
- בדוק dependencies

## Resources

- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [Cohere API](https://docs.cohere.com/)
- [Python Best Practices](https://docs.python-guide.org/)
