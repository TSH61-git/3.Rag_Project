# 🚀 הוראות שימוש מהירות

## התחלה מהירה (3 שלבים)

### 1️⃣ התקנה
```bash
pip install -r requirements.txt
```

### 2️⃣ הגדרת מפתח API
צור קובץ `.env`:
```bash
COHERE_API_KEY=your_key_here
```

### 3️⃣ הרצה
```bash
# Windows
start.bat

# או ידנית
python build_index.py
python app.py
```

פתח דפדפן: `http://127.0.0.1:7860`

---

## תיעוד אוטומטי

### עדכון חד-פעמי
```bash
# Windows
update_docs.bat

# או ידנית
python scripts/generate_docs.py
```

### ניטור רציף
```bash
# Windows
monitor_docs.bat

# או ידנית
python scripts/doc_monitor.py
```

---

## תיעוד מלא

כל התיעוד נמצא ב-[docs/](docs/):

| קובץ | תיאור |
|------|-------|
| [README.md](docs/README.md) | אינדקס תיעוד |
| [INSTALLATION.md](docs/INSTALLATION.md) | התקנה |
| [USAGE.md](docs/USAGE.md) | שימוש |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | ארכיטקטורה |
| [API.md](docs/API.md) | API |
| [FAQ.md](docs/FAQ.md) | שאלות נפוצות |

---

## דוגמאות שאילתות

```
"מה הצבע העיקרי בדיזיין?"
"רשום את כל ההחלטות הטכניות"
"איך מתקינים את המערכת?"
"הסבר את הארכיטקטורה"
```

---

## פתרון בעיות מהיר

### "COHERE_API_KEY not found"
```bash
echo COHERE_API_KEY=your_key > .env
```

### "Index not found"
```bash
python build_index.py
```

### "Port already in use"
```python
# app.py - שנה פורט
demo.launch(server_port=7861)
```

ראה [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) למידע נוסף.

---

## קישורים שימושיים

- 📚 [תיעוד מלא](docs/)
- 🔄 [תיעוד אוטומטי](docs/AUTO_DOCUMENTATION.md)
- 📋 [סיכום](DOCUMENTATION_SUMMARY.md)
