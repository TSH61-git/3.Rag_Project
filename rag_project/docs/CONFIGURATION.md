# ⚙️ מדריך הגדרות

## קובץ הגדרות ראשי

**קובץ:** `src/config.py`

```python
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
STORAGE_DIR = "data/storage"
DOCS_PATHS = {
    "cursor": "mock_docs/cursor",
    "claude_code": "mock_docs/claude_code",
    "task_manager_docs": "mock_docs/task-manager-api/docs"
}
CHUNK_SIZE = 256
CHUNK_OVERLAP = 50
```

## הגדרות מפורטות

### 1. מקורות מסמכים

#### הוספת תיקייה חדשה
```python
DOCS_PATHS = {
    "cursor": "mock_docs/cursor",
    "my_new_docs": "path/to/new/docs"  # הוסף כאן
}
```

### 2. Chunking

#### CHUNK_SIZE (ברירת מחדל: 256)
- **128-256:** דיוק גבוה
- **512-1024:** הקשר רחב

#### CHUNK_OVERLAP (ברירת מחדל: 50)
- **50-100:** שמירת הקשר
- **0-25:** פחות כפילויות

### 3. Retrieval

```python
TOP_K = 3  # ניסיון ראשון
TOP_K_RETRY = 5  # retry
```

### 4. LLM Settings

```python
llm = Cohere(
    model="command-r-plus-08-2024",
    temperature=0.1  # דטרמיניסטי
)
```

**מודלים:**
- `command-r-plus-08-2024` - הכי חזק
- `command-r-08-2024` - מהיר
- `command-r` - בסיסי

### 5. Workflow

```python
workflow = SyncRAGWorkflow(
    index=index,
    max_attempts=2  # 1-3 מומלץ
)
```

### 6. Confidence Thresholds

```python
if confidence >= 0.3:
    return "continue"
elif confidence >= 0.15:
    return "continue_with_warning"
else:
    return "retry"
```

### 7. Gradio UI

```python
demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    share=False
)
```

## משתני סביבה (.env)

```bash
COHERE_API_KEY=your_key_here
USE_OLLAMA=false
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

## דוגמאות לתרחישים

### מסמכים ארוכים
```python
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200
TOP_K = 5
```

### דיוק מקסימלי
```python
CHUNK_SIZE = 128
TOP_K = 10
HIGH_CONFIDENCE = 0.5
```

### מהירות מקסימלית
```python
CHUNK_SIZE = 512
TOP_K = 3
MAX_ATTEMPTS = 1
```

## המלצות

### פרויקטים קטנים (<100 מסמכים)
```python
CHUNK_SIZE = 256
TOP_K = 3
```

### פרויקטים בינוניים (100-1000)
```python
CHUNK_SIZE = 512
TOP_K = 5
```

### פרויקטים גדולים (>1000)
```python
CHUNK_SIZE = 1024
TOP_K = 10
```
