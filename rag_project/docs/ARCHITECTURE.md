# 🏗️ ארכיטקטורה - RAG Documentation Assistant

## סקירה כללית
מערכת RAG מתקדמת לניתוח ושאילתות על תיעוד פרויקטים, עם ניתוב חכם ועדכון אוטומטי.

## רכיבים עיקריים

### 1. שכבת טעינה (Data Loading)
**קובץ:** `src/data_loader.py`
- טעינת מסמכים מתיקיות מרובות
- תמיכה בפורמטים: Markdown, Text, JSON
- סינון קבצים לפי סוג

### 2. שכבת אינדוקס (Indexing)
**קובץ:** `src/indexer.py`
- חיתוך מסמכים ל-chunks (256 תווים)
- יצירת embeddings עם Cohere
- אחסון ב-VectorStoreIndex מקומי

### 3. שכבת Workflow
**קובץ:** `src/sync_event_workflow_v2.py`

#### שלבי Workflow:
```
Input → Validation → Routing → [Semantic/Structured] → Quality Check → LLM → Response
```

**שלבים:**
1. **Input Validation** - אימות קלט ואתחול state
2. **Query Routing** - ניתוב לפי סוג שאילתה
3. **Node Retrieval** - שליפת מסמכים רלוונטיים
4. **Quality Check** - בדיקת איכות + retry logic
5. **LLM Synthesis** - סינתזה עם Cohere
6. **Response Formatting** - עיצוב תשובה סופית

### 4. שכבת ניתוב (Routing)
**קבצים:**
- `src/routing/query_router.py` - ניתוב שאילתות
- `src/classification/query_classifier.py` - סיווג שאילתות

**סוגי שאילתות:**
- **Semantic** - שאלות פתוחות, הסברים
- **Structured** - רשימות, סינונים, נתונים מובנים

### 5. שכבת חילוץ נתונים (Extraction)
**קבצים:**
- `src/extraction/extractor.py` - חילוץ נתונים מובנים
- `src/extraction/schema.py` - הגדרות סכמות
- `src/extraction/structured_query.py` - שאילתות מובנות

## זרימת נתונים

```
User Query
    ↓
Input Validation
    ↓
Query Router
    ↓
[Semantic Path]     [Structured Path]
    ↓                      ↓
Node Retrieval      Data Extraction
    ↓                      ↓
    └──────→ Quality Check ←──────┘
                ↓
         [High Confidence]  [Low Confidence]
                ↓                  ↓
         LLM Synthesis         Retry (max 2)
                ↓
         Response Formatting
                ↓
         User Response
```

## אחסון

### מבנה תיקיות:
```
data/
├── storage/
│   ├── default__vector_store.json  # Vector embeddings
│   ├── docstore.json                # מסמכים מקוריים
│   ├── index_store.json             # מטא-דאטה של אינדקס
│   └── graph_store.json             # קשרים בין מסמכים
└── extracted_data.json              # נתונים מחולצים
```

## טכנולוגיות

| רכיב | טכנולוגיה | תפקיד |
|------|-----------|-------|
| Framework | LlamaIndex | ניהול RAG workflow |
| Embeddings | Cohere | המרת טקסט לוקטורים |
| LLM | Cohere (command-r-plus) | סינתזת תשובות |
| UI | Gradio | ממשק משתמש |
| Storage | JSON Files | אחסון מקומי |

## הגדרות

**קובץ:** `src/config.py`

```python
CHUNK_SIZE = 256        # גודל chunk
CHUNK_OVERLAP = 50      # חפיפה בין chunks
STORAGE_DIR = "data/storage"
```

## ביצועים

- **זמן אינדוקס:** ~2-5 שניות
- **זמן שאילתה:** ~1-3 שניות
- **Retry Logic:** עד 2 ניסיונות
- **Top-K Retrieval:** 3-5 מסמכים

## אבטחה

- מפתחות API ב-`.env` בלבד
- אין שמירת היסטוריית שיחות
- אחסון מקומי בלבד
