# 📊 RAG Documentation Assistant

## תיאור הפרויקט
מערכת RAG שמאפשרת לתשאל ולהפיק תובנות מקבצי התיעוד של כלי Agentic Coding (Cursor, Claude Code וכו').

## 📚 תיעוד מלא

כל התיעוד נמצא בתיקיית [docs/](docs/):

- 🚀 [מדריך התקנה](docs/INSTALLATION.md)
- 📖 [מדריך שימוש](docs/USAGE.md)
- 🏗️ [ארכיטקטורה](docs/ARCHITECTURE.md)
- 🔄 [Workflow](docs/WORKFLOW.md)
- 📡 [API](docs/API.md)
- ⚙️ [הגדרות](docs/CONFIGURATION.md)
- 🛠️ [פיתוח](docs/DEVELOPMENT.md)
- ❓ [שאלות נפוצות](docs/FAQ.md)
- 🔧 [פתרון בעיות](docs/TROUBLESHOOTING.md)
- 🔄 [תיעוד אוטומטי](docs/AUTO_DOCUMENTATION.md)

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

## שלב ב' - Event-Driven Workflow (✅ מושלם)

הארכיטקטורה שודרגה ל-Workflow Event-Driven מלא עם:

### תכונות מתקדמות:
- **ניתוב דינמי** - הזרימה משתנה לפי איכות התוצאות
- **State Management** - עוקב אחרי ניסיונות והיסטוריה
- **Retry אוטומטי** - אם confidence נמוך, מנסה שוב עם יותר הקשר
- **ולידציות מרובות** - בדיקות בכל שלב
- **Fallback חכם** - אם LLM נכשל, מחזיר תוכן גולמי

### 5 Steps:
1. **Input Validation** - אימות קלט + אתחול State
2. **Node Retrieval** - שליפה (3 nodes → 5 nodes בretry)
3. **Quality Check** - הערכה + ניתוב (continue/retry/stop)
4. **LLM Synthesis** - סינתזה עם Cohere (3 מודלים)
5. **Response Formatting** - עיצוב + metadata

### ניתוב לפי Confidence:
```
confidence >= 0.3  → ✅ המשך
confidence >= 0.15 → ⚠️ המשך עם אזהרה
confidence < 0.15  → 🔄 retry (max 2 attempts)
```

ראה [STAGE_B_COMPLETE.md](STAGE_B_COMPLETE.md) לתיעוד מלא.

## שלב ג' - Data Extraction (בפיתוח)
בשלב זה נוסיף חילוץ נתונים מובנה לשאלות מורכבות.

## הערות
- קבצי ה-md במערכת הם לדוגמה בלבד
- במערכת אמיתית, יש לסנכרן את האינדקס עם שינויים בקבצים
- ניתן להוסיף כלי Agentic Coding נוספים ב-config.py
