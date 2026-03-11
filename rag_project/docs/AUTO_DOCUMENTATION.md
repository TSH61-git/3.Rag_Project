# 🔄 מערכת ניטור ועדכון תיעוד אוטומטי

## סקירה כללית

המערכת כוללת שני כלים לניהול תיעוד אוטומטי:

### 1. מחולל תיעוד (Generate Docs)
סורק את הקוד ומייצר תיעוד מפורט

### 2. ניטור שינויים (Doc Monitor)
עוקב אחרי שינויים בזמן אמת ומעדכן תיעוד

---

## שימוש מהיר

### יצירת תיעוד חד-פעמי
```bash
python scripts/generate_docs.py
```

**מה זה יוצר:**
- `docs/MODULE_INDEX.md` - אינדקס כל המודולים
- `docs/FUNCTION_REFERENCE.md` - מדריך פונקציות
- `docs/CLASS_REFERENCE.md` - מדריך מחלקות

### הפעלת ניטור רציף
```bash
python scripts/doc_monitor.py
```

**מה זה עושה:**
- עוקב אחרי שינויים בקבצים
- מעדכן `MODULE_INDEX.md` אוטומטית
- רושם שינויים ב-`CHANGES.md`
- מזהה פונקציות ומחלקות חדשות

---

## דוגמאות

### דוגמה 1: עריכת קובץ Python
```bash
# הפעל ניטור
python scripts/doc_monitor.py

# ערוך קובץ
# src/my_module.py

# התיעוד יתעדכן אוטומטית!
```

### דוגמה 2: הוספת מודול חדש
```bash
# צור קובץ חדש
# src/new_feature.py

# הרץ מחולל
python scripts/generate_docs.py

# בדוק תיעוד
cat docs/MODULE_INDEX.md
```

---

## קבצי תיעוד שנוצרים

| קובץ | תיאור | עדכון |
|------|-------|--------|
| `MODULE_INDEX.md` | אינדקס מודולים | אוטומטי |
| `FUNCTION_REFERENCE.md` | מדריך פונקציות | ידני |
| `CLASS_REFERENCE.md` | מדריך מחלקות | ידני |
| `CHANGES.md` | יומן שינויים | אוטומטי |

---

## הגדרות מתקדמות

### שינוי תדירות עדכון
```python
# scripts/doc_monitor.py
time.sleep(1)  # בדיקה כל שנייה
```

### התעלמות מקבצים
```python
# scripts/doc_monitor.py
ignore_patterns = [
    '.pyc', '__pycache__', '.git', 
    'venv', 'node_modules', '.env'
]
```

### הוספת סוגי קבצים
```python
# scripts/doc_monitor.py
if file_path.suffix in ['.py', '.md', '.txt', '.json']:
    self._update_documentation(file_path)
```

---

## Workflow מומלץ

### פיתוח יומיומי
1. הפעל ניטור בטרמינל נפרד:
   ```bash
   python scripts/doc_monitor.py
   ```

2. עבוד על הקוד כרגיל

3. התיעוד יתעדכן אוטומטית

### לפני Commit
```bash
# עדכן תיעוד
python scripts/generate_docs.py

# בדוק שינויים
git diff docs/

# Commit
git add docs/
git commit -m "Update documentation"
```

---

## בדיקת תיעוד

### בדיקה מהירה
```bash
# בדוק אם קבצים נוצרו
ls docs/

# קרא תיעוד
cat docs/MODULE_INDEX.md
```

### בדיקה מלאה
```bash
# הרץ מחולל
python scripts/generate_docs.py

# בדוק כל קובץ
for file in docs/*.md; do
    echo "=== $file ==="
    head -n 20 "$file"
done
```

---

## פתרון בעיות

### "No module named 'watchdog'"
```bash
pip install watchdog
```

### "Permission denied"
```bash
chmod +x scripts/*.py
```

### תיעוד לא מתעדכן
```bash
# הרץ מחדש
python scripts/generate_docs.py

# בדוק לוגים
python scripts/doc_monitor.py --verbose
```

---

## טיפים

1. **הפעל ניטור בפיתוח** - תמיד תהיה לך תיעוד מעודכן
2. **הרץ מחולל לפני release** - ודא שהתיעוד מלא
3. **בדוק CHANGES.md** - עקוב אחרי שינויים
4. **התאם ignore_patterns** - התעלם מקבצים לא רלוונטיים

---

## אינטגרציה עם CI/CD

### GitHub Actions
```yaml
# .github/workflows/docs.yml
name: Update Docs
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python scripts/generate_docs.py
      - run: git add docs/
      - run: git commit -m "Auto-update docs"
      - run: git push
```

---

## שלבים הבאים

1. ✅ הפעל ניטור
2. 📝 ערוך קוד
3. 🔍 בדוק תיעוד
4. 🚀 Commit שינויים
