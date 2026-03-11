# 🤝 מדריך תרומה

## ברוכים הבאים!

תודה על העניין לתרום לפרויקט! כל תרומה מוערכת.

---

## איך לתרום?

### 1. Fork הפרויקט
```bash
# לחץ על "Fork" ב-GitHub
```

### 2. Clone לוקאלי
```bash
git clone https://github.com/YOUR_USERNAME/rag_project.git
cd rag_project
```

### 3. צור ענף חדש
```bash
git checkout -b feature/my-awesome-feature
```

### 4. התקן תלויות פיתוח
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 5. עשה שינויים
```bash
# ערוך קבצים
# הוסף תכונות
# תקן באגים
```

### 6. הרץ בדיקות
```bash
pytest tests/
```

### 7. עדכן תיעוד
```bash
python scripts/generate_docs.py
```

### 8. Commit
```bash
git add .
git commit -m "Add: my awesome feature"
```

### 9. Push
```bash
git push origin feature/my-awesome-feature
```

### 10. צור Pull Request
```bash
# לך ל-GitHub וצור PR
```

---

## סוגי תרומות

### 🐛 דיווח על באגים
1. בדוק אם הבאג כבר דווח
2. צור Issue חדש
3. כלול:
   - תיאור הבעיה
   - שלבים לשחזור
   - לוגים/שגיאות
   - גרסת Python

### 💡 הצעות לתכונות
1. צור Feature Request
2. תאר את התכונה
3. הסבר מקרי שימוש
4. הוסף דוגמאות

### 📖 שיפור תיעוד
1. מצאת טעות? תקן!
2. חסר מידע? הוסף!
3. לא ברור? הבהר!

### 🔧 תיקון באגים
1. מצא באג ב-Issues
2. הצע פתרון
3. כתוב בדיקה
4. שלח PR

### ✨ תכונות חדשות
1. דון ב-Discussions
2. קבל אישור
3. מימש
4. תעד
5. שלח PR

---

## קונבנציות

### Commit Messages
```bash
# פורמט
Type: Short description

# סוגים
Add: תכונה חדשה
Fix: תיקון באג
Update: עדכון קוד קיים
Docs: שינוי בתיעוד
Test: הוספת בדיקות
Refactor: שיפור קוד

# דוגמאות
Add: query routing feature
Fix: index loading error
Update: improve performance
Docs: add API examples
```

### Code Style
```python
# PEP 8
# Type hints
# Docstrings

def my_function(param: str, count: int = 5) -> List[str]:
    """
    תיאור הפונקציה
    
    Args:
        param: תיאור
        count: מספר
        
    Returns:
        רשימה
    """
    return ["result"] * count
```

### בדיקות
```python
# tests/test_my_feature.py
import pytest

def test_my_feature():
    """בדיקת התכונה שלי"""
    result = my_feature("test")
    assert result == "expected"
```

---

## Checklist לפני PR

- [ ] הקוד עובד
- [ ] בדיקות עוברות
- [ ] תיעוד מעודכן
- [ ] Commit messages תקינים
- [ ] אין קונפליקטים
- [ ] Code style תקין

---

## תהליך Review

1. **Submit PR** - שלח את ה-PR
2. **Automated Tests** - בדיקות אוטומטיות
3. **Code Review** - סקירת קוד
4. **Changes Requested** - שינויים נדרשים (אם יש)
5. **Approval** - אישור
6. **Merge** - מיזוג לפרויקט

---

## קהילה

### תקשורת
- 💬 GitHub Discussions - שאלות כלליות
- 🐛 GitHub Issues - באגים ותכונות
- 📧 Email - שאלות פרטיות

### כללי התנהגות
- 🤝 כבד אחרים
- 💡 היה בונה
- 🎯 היה ממוקד
- 📚 למד ולמד אחרים

---

## רעיונות לתרומה

### קל
- [ ] תיקון טעויות כתיב
- [ ] שיפור דוגמאות
- [ ] הוספת תרגומים
- [ ] עדכון תיעוד

### בינוני
- [ ] הוספת בדיקות
- [ ] שיפור ביצועים
- [ ] תיקון באגים
- [ ] הוספת דוגמאות

### מתקדם
- [ ] תכונות חדשות
- [ ] אינטגרציות
- [ ] אופטימיזציות
- [ ] ארכיטקטורה

---

## משאבים

### תיעוד
- [DEVELOPMENT.md](docs/DEVELOPMENT.md)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [API.md](docs/API.md)

### כלים
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [Cohere API](https://docs.cohere.com/)
- [Python Best Practices](https://docs.python-guide.org/)

---

## שאלות?

יש שאלות? אל תהסס לשאול!
- 💬 GitHub Discussions
- 📧 Email
- 🐛 GitHub Issues

---

**תודה על התרומה! 🎉**
