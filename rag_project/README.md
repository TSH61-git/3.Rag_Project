# 📊 RAG Documentation Assistant

## תיאור הפרויקט
מערכת RAG שמאפשרת לתשאל ולהפיק תובנות מקבצי התיעוד של כלי Agentic Coding (Cursor, Claude Code וכו').

## שלב א' - MVP: תשאול סמנטי עם Embeddings

### טכנולוגיות
- **LlamaIndex**: Framework לבניית יישומי RAG
- **Cohere**: מודל Embeddings ו-LLM (command-r)
- **אחסון מקומי**: Vector store בקבצי JSON
- **Gradio**: ממשק משתמש

### התקנה

1. התקן את התלויות:
```bash
pip install -r requirements.txt
```

2. צור קובץ `.env` והוסף את מפתח Cohere:
```bash
COHERE_API_KEY=your_key_here
```

3. בנה את האינדקס (פעם אחת):
```bash
python build_index.py
```

4. הרץ את האפליקציה:
```bash
python app.py
```

### ארכיטקטורה

```
1. Loading (data_loader.py)
   ↓
2. Chunking (indexer.py - SentenceSplitter)
   ↓
3. Embedding (indexer.py - CohereEmbedding)
   ↓
4. VectorStoreIndex (indexer.py)
   ↓
5. Local Storage (data/storage/)
   ↓
6. Workflow (rag_workflow.py):
   - Input Validation
   - Node Retrieval
   - Quality Check
   - LLM Synthesis (Cohere)
   - Response Formatting
   ↓
7. Gradio UI (app.py)
```

### דוגמאות לשאלות

✅ **שאלות שהמערכת יודעת לענות:**

- "מה הצבע העיקרי שנבחר לדיזיין של המערכת?"
- "לאילו שפות הוחלט לתרגם את הכיתובים בממשק?"
- "האם נעשה שינוי במבנה ה-DB בחודש האחרון?"
- "אילו שדות נוספו או הוסרו מטבלאות קיימות?"
- "האם קיימת הנחיה עקבית לגבי שימוש ב-RTL בממשק?"
- "איזה רכיב במערכת הוגדר כבעייתי או רגיש במיוחד?"
- "איך מתקינים את המערכת?"
- "מה ההחלטות הטכניות שהתקבלו?"

### מבנה הפרויקט

```
rag_project/
├── mock_docs/              # קבצי תיעוד לדוגמה
│   ├── cursor/
│   │   ├── spec.md
│   │   ├── instructions.md
│   │   └── tasks.md
│   └── claude_code/
│       ├── plan.md
│       ├── decisions.md
│       └── README.md
├── src/
│   ├── config.py          # הגדרות
│   ├── data_loader.py     # טעינת מסמכים
│   ├── indexer.py         # יצירת אינדקס
│   └── query_engine.py    # מנוע שאילתות
├── build_index.py         # סקריפט לבניית אינדקס
├── app.py                 # ממשק Gradio
├── requirements.txt
└── README.md
```

## שלב ב' - Event-Driven Workflow (✅ הושלם)
הארכיטקטורה שודרגה ל-Workflow מבוסס אירועים עם 5 שלבים:
1. **Input Validation** - אימות קלט
2. **Node Retrieval** - שליפת nodes רלוונטיים
3. **Quality Check** - בדיקת איכות התוצאות
4. **LLM Synthesis** - סינתזה של תשובה עם Cohere LLM
5. **Response Formatting** - עיצוב התשובה הסופית

## שלב ג' - Data Extraction (בפיתוח)
בשלב זה נוסיף חילוץ נתונים מובנה לשאלות מורכבות.

## הערות
- קבצי ה-md במערכת הם לדוגמה בלבד
- במערכת אמיתית, יש לסנכרן את האינדקס עם שינויים בקבצים
- ניתן להוסיף כלי Agentic Coding נוספים ב-config.py
