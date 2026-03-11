# 🚀 מדריך התקנה

## דרישות מקדימות

- Python 3.8+
- pip
- חשבון Cohere (חינם)

## התקנה מהירה

### 1. סביבה וירטואלית
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. התקנת תלויות
```bash
pip install -r requirements.txt
```

### 3. הגדרת .env
```bash
COHERE_API_KEY=your_key_here
```

**השגת מפתח:**
1. [Cohere Dashboard](https://dashboard.cohere.com)
2. API Keys → צור מפתח חדש

### 4. בניית אינדקס
```bash
python build_index.py
```

### 5. הרצה
```bash
python app.py
```

פתח: `http://127.0.0.1:7860`

## התקנה עם Ollama (מקומי)

```bash
# התקן Ollama
winget install Ollama.Ollama

# הורד מודל
ollama pull llama3.2

# עדכן config.py
USE_OLLAMA = True
```

## בדיקת התקנה

```bash
python test_query.py
python test_keys.py
```

## פתרון בעיות

### "No module named 'llama_index'"
```bash
pip install --upgrade llama-index-core
```

### "COHERE_API_KEY not found"
- ודא שקובץ `.env` קיים
- בדוק שאין רווחים במפתח

### "Index not found"
```bash
python build_index.py
```

### "Port 7860 already in use"
```python
# app.py
demo.launch(server_port=7861)
```

## עדכון

```bash
pip install --upgrade -r requirements.txt
rm -rf data/storage/*
python build_index.py
```

## מבנה אחרי התקנה

```
rag_project/
├── venv/
├── data/storage/  # נוצר אוטומטית
├── .env           # צור ידנית
└── app.py
```
