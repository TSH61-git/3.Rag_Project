# ❓ שאלות נפוצות (FAQ)

## כללי

### מה זה RAG?
RAG (Retrieval-Augmented Generation) היא טכניקה המשלבת שליפת מידע עם יצירת טקסט. המערכת שולפת מסמכים רלוונטיים ומשתמשת בהם כהקשר ליצירת תשובות מדויקות.

### למה להשתמש במערכת הזו?
- 📚 תשאול מסמכים בשפה טבעית
- 🎯 תשובות מדויקות מבוססות על התיעוד שלך
- 🔄 עדכון אוטומטי של האינדקס
- 🚀 קל להתקנה ולשימוש

### האם זה חינמי?
המערכת עצמה חינמית. תצטרך:
- ✅ Cohere API (חינם עד 100 קריאות/דקה)
- ✅ או Ollama (לגמרי חינמי, מקומי)

---

## התקנה

### איך מתקינים?
```bash
pip install -r requirements.txt
python build_index.py
python app.py
```
ראה [INSTALLATION.md](INSTALLATION.md) למדריך מלא.

### מה עושים אם ההתקנה נכשלת?
1. ודא Python 3.8+
2. עדכן pip: `pip install --upgrade pip`
3. נסה סביבה וירטואלית: `python -m venv venv`

### איך משיגים מפתח Cohere?
1. היכנס ל-[Cohere Dashboard](https://dashboard.cohere.com)
2. לחץ "API Keys"
3. צור מפתח חדש
4. הדבק ב-`.env`

---

## שימוש

### איך שואלים שאלות?
פשוט כתוב בשפה טבעית:
- "מה הצבע העיקרי?"
- "רשום את כל ההחלטות"
- "הסבר את הארכיטקטורה"

### מה ההבדל בין שאילתות סמנטיות למובנות?
- **סמנטיות:** שאלות פתוחות ("הסבר...", "מה...")
- **מובנות:** רשימות ונתונים ("רשום...", "הצג...")

### איך משפרים את התשובות?
1. הוסף יותר מסמכים
2. שנה `CHUNK_SIZE` ב-config
3. הגדל `TOP_K` לשליפת יותר מסמכים
4. בנה אינדקס מחדש

---

## הגדרות

### איך משנים את גודל ה-chunks?
```python
# src/config.py
CHUNK_SIZE = 512  # במקום 256
```

### איך מוסיפים תיקיית מסמכים?
```python
# src/config.py
DOCS_PATHS = {
    "cursor": "mock_docs/cursor",
    "my_docs": "path/to/my/docs"  # הוסף כאן
}
```

### איך משנים את המודל?
```python
# src/sync_event_workflow_v2.py
llm = Cohere(
    model="command-r-08-2024",  # מודל אחר
    temperature=0.3
)
```

---

## בעיות נפוצות

### "COHERE_API_KEY not found"
**פתרון:**
1. צור קובץ `.env` בתיקיית הפרויקט
2. הוסף: `COHERE_API_KEY=your_key_here`
3. ודא שאין רווחים

### "Index not found"
**פתרון:**
```bash
python build_index.py
```

### תשובות לא רלוונטיות
**פתרון:**
1. בנה אינדקס מחדש
2. הוסף יותר מסמכים
3. שנה `CHUNK_SIZE` ל-128 (דיוק גבוה יותר)

### המערכת איטית
**פתרון:**
1. השתמש ב-Ollama (מקומי)
2. הקטן `TOP_K` ל-3
3. הפחת `MAX_ATTEMPTS` ל-1

### "Port 7860 already in use"
**פתרון:**
```python
# app.py
demo.launch(server_port=7861)
```

---

## תכונות מתקדמות

### איך משתמשים ב-Ollama?
```bash
# התקן Ollama
winget install Ollama.Ollama

# הורד מודל
ollama pull llama3.2

# עדכן config
USE_OLLAMA = True
```
ראה [OLLAMA_SETUP.md](../OLLAMA_SETUP.md)

### איך מפעילים ניטור אוטומטי?
```bash
python scripts/doc_monitor.py
```
המערכת תעקוב אחרי שינויים ותעדכן תיעוד אוטומטית.

### איך מוסיפים סוג מסמך חדש?
```python
# src/data_loader.py
SUPPORTED_EXTENSIONS = ['.md', '.txt', '.pdf']  # הוסף .pdf
```

---

## ביצועים

### כמה זמן לוקח לבנות אינדקס?
- פרויקט קטן (<50 מסמכים): 2-5 שניות
- פרויקט בינוני (50-200): 10-30 שניות
- פרויקט גדול (>200): 1-3 דקות

### כמה זמן לוקחת שאילתה?
בממוצע 1-3 שניות:
- Retrieval: 0.2-0.5s
- LLM: 0.8-2.5s

### איך מאיצים את המערכת?
```python
CHUNK_SIZE = 512  # chunks גדולים יותר
TOP_K = 3         # פחות מסמכים
MAX_ATTEMPTS = 1  # פחות retries
```

---

## אבטחה

### האם המידע שלי מאובטח?
✅ כל הנתונים נשמרים מקומית
✅ אין שליחת מידע לשרתים (מלבד API calls)
✅ מפתחות ב-`.env` בלבד

### מה נשלח ל-Cohere?
רק השאילתה והקונטקסט הרלוונטי (3-5 chunks).
המסמכים המלאים נשארים מקומיים.

### איך מוחקים את ההיסטוריה?
```bash
rm -rf data/storage/*
python build_index.py
```

---

## פיתוח

### איך תורמים לפרויקט?
1. Fork הפרויקט
2. צור ענף: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/my-feature`
5. צור Pull Request

### איך מריצים בדיקות?
```bash
pytest tests/
```

### איך מוסיפים תכונה חדשה?
ראה [DEVELOPMENT.md](DEVELOPMENT.md)

---

## תמיכה

### איפה מוצאים עזרה?
- 📖 [Documentation](.)
- 🐛 [GitHub Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

### איך מדווחים על באג?
1. בדוק אם הבאג כבר דווח
2. צור Issue חדש
3. כלול:
   - תיאור הבעיה
   - שלבים לשחזור
   - לוגים/שגיאות
   - גרסת Python

### איך מבקשים תכונה חדשה?
צור Feature Request ב-GitHub Issues עם:
- תיאור התכונה
- מקרי שימוש
- דוגמאות
