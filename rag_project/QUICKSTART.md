# 🚀 Quick Start Guide

## צעדים להתקנה והרצה

### 1. הכנת הסביבה

```bash
cd rag_project
python -m venv venv
venv\Scripts\activate  # Windows
# או: source venv/bin/activate  # Mac/Linux
```

### 2. התקנת חבילות

```bash
pip install -r requirements.txt
```

### 3. הגדרת מפתחות API

צור קובץ `.env` והעתק את התוכן מ-`.env.example`:

```bash
copy .env.example .env  # Windows
# או: cp .env.example .env  # Mac/Linux
```

ערוך את `.env` והוסף את המפתחות שלך:

#### איך להשיג מפתחות?

**Cohere:**
1. היכנס ל-https://dashboard.cohere.com/
2. הירשם/התחבר
3. לך ל-API Keys
4. העתק את ה-API Key

**Pinecone:**
1. היכנס ל-https://www.pinecone.io/
2. הירשם/התחבר
3. צור פרויקט חדש
4. לך ל-API Keys
5. העתק את ה-API Key וה-Environment

### 4. בניית האינדקס (פעם אחת)

```bash
python build_index.py
```

זה ייקח כמה דקות. התהליך:
- טוען את כל קבצי ה-MD
- חותך אותם ל-chunks
- יוצר embeddings
- שומר ב-Pinecone

### 5. הרצת האפליקציה

```bash
python app.py
```

הממשק ייפתח בדפדפן בכתובת: http://localhost:7860

## 🎯 דוגמאות לשאלות

נסי לשאול:
- "מה הצבע העיקרי בעיצוב?"
- "אילו שפות נתמכות?"
- "מה השינויים האחרונים ב-DB?"
- "מה הכללים ל-RTL?"
- "איזה חלקים רגישים במערכת?"

## 🔧 פתרון בעיות

### שגיאה: "No module named 'llama_index'"
```bash
pip install --upgrade llama-index
```

### שגיאה: "Pinecone index not found"
הרץ שוב את `python build_index.py`

### שגיאה: "Invalid API key"
בדוק שהמפתחות ב-`.env` נכונים

## 📁 מבנה הפרויקט

```
rag_project/
├── mock_docs/          # קבצי MD לדוגמה
├── src/                # קוד המערכת
├── app.py              # ממשק Gradio
├── build_index.py      # בניית אינדקס
└── requirements.txt    # תלויות
```

## ⏭️ השלבים הבאים

לאחר שהמערכת עובדת:
1. **שלב ב'**: שדרוג ל-Event-Driven Architecture
2. **שלב ג'**: הוספת Data Extraction למידע מובנה

---

💡 **טיפ**: אם יש לך קבצי MD אמיתיים מ-Cursor/Claude Code, פשוט החלף את התיקיות ב-`mock_docs/` והרץ שוב את `build_index.py`
