# 🔧 פתרון בעיות

## בעיות התקנה

### "No module named 'llama_index'"
**סיבה:** חבילות לא מותקנות

**פתרון:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Python version not supported"
**סיבה:** Python ישן מדי

**פתרון:**
```bash
python --version  # צריך להיות 3.8+
# התקן Python 3.8 ומעלה
```

### "Permission denied"
**סיבה:** הרשאות חסרות

**פתרון:**
```bash
# Windows: הרץ כמנהל
# Linux/Mac:
sudo pip install -r requirements.txt
```

---

## בעיות API

### "COHERE_API_KEY not found"
**סיבה:** קובץ .env חסר או שגוי

**פתרון:**
```bash
# צור קובץ .env
echo "COHERE_API_KEY=your_key_here" > .env

# ודא שהקובץ בתיקייה הנכונה
ls -la .env
```

### "API rate limit exceeded"
**סיבה:** חרגת ממכסת API

**פתרון:**
1. חכה 60 שניות
2. או השתמש ב-Ollama:
```python
USE_OLLAMA = True
```

### "Invalid API key"
**סיבה:** מפתח שגוי

**פתרון:**
1. בדוק ב-[Cohere Dashboard](https://dashboard.cohere.com)
2. צור מפתח חדש
3. עדכן ב-.env

---

## בעיות אינדקס

### "Index not found"
**סיבה:** אינדקס לא נבנה

**פתרון:**
```bash
python build_index.py
```

### "Index corrupted"
**סיבה:** קבצי אינדקס פגומים

**פתרון:**
```bash
rm -rf data/storage/*
python build_index.py
```

### "Out of memory during indexing"
**סיבה:** יותר מדי מסמכים

**פתרון:**
```python
# הקטן CHUNK_SIZE
CHUNK_SIZE = 128

# או הפחת מסמכים
DOCS_PATHS = {
    "cursor": "mock_docs/cursor"  # רק אחד
}
```

---

## בעיות שאילתות

### תשובות לא רלוונטיות
**סיבות אפשריות:**
1. אינדקס לא מעודכן
2. CHUNK_SIZE גדול מדי
3. מעט מדי מסמכים

**פתרון:**
```bash
# 1. בנה אינדקס מחדש
python build_index.py

# 2. שנה הגדרות
# config.py
CHUNK_SIZE = 128
TOP_K = 10
```

### "No results found"
**סיבה:** שאילתה לא תואמת למסמכים

**פתרון:**
1. נסח שאלה אחרת
2. הוסף מסמכים רלוונטיים
3. הקטן `HIGH_CONFIDENCE`

### תשובות איטיות
**סיבות:**
1. חיבור אינטרנט איטי
2. יותר מדי retries
3. מודל כבד

**פתרון:**
```python
# השתמש ב-Ollama (מקומי)
USE_OLLAMA = True

# הפחת retries
MAX_ATTEMPTS = 1

# הקטן TOP_K
TOP_K = 3
```

---

## בעיות ממשק

### "Port 7860 already in use"
**סיבה:** פורט תפוס

**פתרון:**
```python
# app.py
demo.launch(server_port=7861)
```

### "Cannot connect to 127.0.0.1:7860"
**סיבה:** שרת לא רץ

**פתרון:**
```bash
# בדוק אם רץ
python app.py

# בדוק לוגים
```

### ממשק לא נטען
**סיבה:** JavaScript error

**פתרון:**
1. נקה cache דפדפן
2. נסה דפדפן אחר
3. בדוק console לשגיאות

---

## בעיות ביצועים

### שימוש גבוה ב-RAM
**פתרון:**
```python
CHUNK_SIZE = 512  # chunks גדולים יותר
TOP_K = 3         # פחות מסמכים
```

### שימוש גבוה ב-CPU
**פתרון:**
```python
# השתמש ב-Cohere במקום Ollama
USE_OLLAMA = False
```

### דיסק מלא
**פתרון:**
```bash
# נקה אינדקס ישן
rm -rf data/storage/*

# נקה cache
rm -rf __pycache__
rm -rf .pytest_cache
```

---

## בעיות Ollama

### "Ollama not found"
**פתרון:**
```bash
# התקן Ollama
winget install Ollama.Ollama

# בדוק התקנה
ollama --version
```

### "Model not found"
**פתרון:**
```bash
# הורד מודל
ollama pull llama3.2

# רשימת מודלים
ollama list
```

### "Ollama connection refused"
**פתרון:**
```bash
# הפעל Ollama
ollama serve

# בדוק פורט
curl http://localhost:11434
```

---

## בעיות Windows

### "venv\Scripts\activate not found"
**פתרון:**
```bash
# צור venv מחדש
python -m venv venv

# הפעל
venv\Scripts\activate.bat
```

### "Path too long"
**פתרון:**
1. העבר פרויקט לנתיב קצר יותר
2. או הפעל Long Path Support

---

## בעיות Linux/Mac

### "Permission denied: .env"
**פתרון:**
```bash
chmod 600 .env
```

### "Command not found: python"
**פתרון:**
```bash
# השתמש ב-python3
python3 app.py
```

---

## Debug Mode

### הפעלת debug
```python
# app.py
import logging
logging.basicConfig(level=logging.DEBUG)

# או
demo.launch(debug=True)
```

### בדיקת state
```python
workflow = SyncRAGWorkflow(index=index, verbose=True)
```

---

## לוגים

### איפה הלוגים?
```bash
# stdout
python app.py

# לקובץ
python app.py > app.log 2>&1
```

### ניתוח לוגים
```bash
# חפש שגיאות
grep ERROR app.log

# חפש warnings
grep WARNING app.log
```

---

## בדיקות אבחון

### בדיקה מהירה
```bash
python test_keys.py
python test_query.py
```

### בדיקה מלאה
```bash
pytest tests/ -v
```

---

## קבלת עזרה

אם הבעיה לא נפתרה:

1. 📖 בדוק [FAQ.md](FAQ.md)
2. 🔍 חפש ב-GitHub Issues
3. 🐛 דווח על באג חדש
4. 💬 שאל ב-Discussions

---

## טיפים למניעת בעיות

1. ✅ השתמש בסביבה וירטואלית
2. ✅ עדכן תלויות באופן קבוע
3. ✅ בנה אינדקס מחדש אחרי שינויים
4. ✅ שמור גיבויים של .env
5. ✅ בדוק לוגים באופן קבוע
