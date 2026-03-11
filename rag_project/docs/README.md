# 📚 אינדקס תיעוד - RAG Documentation Assistant

## ברוכים הבאים!

זהו מדריך התיעוד המלא לפרויקט RAG Documentation Assistant.

---

## 🚀 התחלה מהירה

| מסמך | תיאור |
|------|-------|
| [INSTALLATION.md](INSTALLATION.md) | מדריך התקנה מלא |
| [USAGE.md](USAGE.md) | שימוש מהיר במערכת |
| [QUICKSTART.md](../QUICKSTART.md) | התחלה מהירה |

---

## 📖 תיעוד מפורט

### ארכיטקטורה ועיצוב
- [ARCHITECTURE.md](ARCHITECTURE.md) - ארכיטקטורה מלאה של המערכת
- [WORKFLOW.md](WORKFLOW.md) - תיעוד Workflow מפורט
- [API.md](API.md) - תיעוד API ופונקציות

### הגדרות ותצורה
- [CONFIGURATION.md](CONFIGURATION.md) - מדריך הגדרות מקיף
- [.env.example](../.env.example) - דוגמת קובץ הגדרות

### פיתוח
- [DEVELOPMENT.md](DEVELOPMENT.md) - מדריך למפתחים
- [MODULE_INDEX.md](MODULE_INDEX.md) - אינדקס מודולים (מתעדכן אוטומטית)
- [CHANGES.md](CHANGES.md) - יומן שינויים (מתעדכן אוטומטית)

---

## ❓ עזרה ותמיכה

- [FAQ.md](FAQ.md) - שאלות נפוצות
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - פתרון בעיות

---

## 📋 תיעוד נוסף

### מדריכים מיוחדים
- [OLLAMA_SETUP.md](../OLLAMA_SETUP.md) - הגדרת Ollama (מקומי)
- [OFFLINE_MODE.md](../OFFLINE_MODE.md) - מצב לא מקוון
- [WORKFLOW_DIAGRAM.md](../WORKFLOW_DIAGRAM.md) - דיאגרמת Workflow

### דיאגרמות
- [workflow_diagram.html](../workflow_diagram.html) - דיאגרמה אינטראקטיבית

---

## 🗂️ מבנה התיעוד

```
docs/
├── README.md              # אינדקס זה
├── INSTALLATION.md        # התקנה
├── USAGE.md               # שימוש
├── ARCHITECTURE.md        # ארכיטקטורה
├── WORKFLOW.md            # Workflow
├── API.md                 # API
├── CONFIGURATION.md       # הגדרות
├── DEVELOPMENT.md         # פיתוח
├── FAQ.md                 # שאלות נפוצות
├── TROUBLESHOOTING.md     # פתרון בעיות
├── MODULE_INDEX.md        # אינדקס מודולים (אוטומטי)
└── CHANGES.md             # יומן שינויים (אוטומטי)
```

---

## 🔄 תיעוד אוטומטי

המערכת כוללת מנגנון עדכון תיעוד אוטומטי:

```bash
# הפעל ניטור
python scripts/doc_monitor.py
```

**מה זה עושה:**
- עוקב אחרי שינויים בקבצים
- מעדכן את `MODULE_INDEX.md` אוטומטית
- רושם שינויים ב-`CHANGES.md`
- מזהה פונקציות ומחלקות חדשות

---

## 📊 סטטיסטיקות פרויקט

| מדד | ערך |
|-----|-----|
| קבצי Python | 15+ |
| מודולים | 6 |
| מסמכי תיעוד | 10+ |
| שורות קוד | ~2000 |

---

## 🎯 מסלולי למידה

### למתחילים
1. [INSTALLATION.md](INSTALLATION.md) - התקנה
2. [USAGE.md](USAGE.md) - שימוש בסיסי
3. [FAQ.md](FAQ.md) - שאלות נפוצות

### למשתמשים מתקדמים
1. [CONFIGURATION.md](CONFIGURATION.md) - התאמה אישית
2. [ARCHITECTURE.md](ARCHITECTURE.md) - הבנת המערכת
3. [WORKFLOW.md](WORKFLOW.md) - Workflow מתקדם

### למפתחים
1. [DEVELOPMENT.md](DEVELOPMENT.md) - הגדרת סביבה
2. [API.md](API.md) - שימוש ב-API
3. [MODULE_INDEX.md](MODULE_INDEX.md) - מבנה הקוד

---

## 🔗 קישורים שימושיים

### תיעוד חיצוני
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Cohere API Docs](https://docs.cohere.com/)
- [Gradio Documentation](https://www.gradio.app/docs/)

### כלים
- [Cohere Dashboard](https://dashboard.cohere.com)
- [Ollama](https://ollama.com)

---

## 📝 הערות

- כל קבצי התיעוד כתובים בעברית
- דוגמאות קוד כוללות הערות
- התיעוד מתעדכן אוטומטית עם הקוד

---

## 🤝 תרומה

רוצה לתרום? ראה [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 📧 יצירת קשר

- 🐛 דיווח על באגים: GitHub Issues
- 💡 הצעות לתכונות: GitHub Discussions
- 📖 שאלות: FAQ.md

---

**עדכון אחרון:** 2024-01-15 12:00
**גרסה:** 1.0.0
