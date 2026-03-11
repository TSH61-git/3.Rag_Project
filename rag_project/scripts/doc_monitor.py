"""
מערכת ניטור קבצים אוטומטית - עדכון תיעוד בזמן אמת
"""
import os
import time
import json
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DocumentationUpdater(FileSystemEventHandler):
    """מעקב אחרי שינויים בקבצים ועדכון תיעוד"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.changes_log = self.docs_dir / "CHANGES.md"
        self.ensure_docs_dir()
        
    def ensure_docs_dir(self):
        """יצירת תיקיית docs אם לא קיימת"""
        self.docs_dir.mkdir(exist_ok=True)
        
    def on_modified(self, event):
        """מופעל כשקובץ משתנה"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # התעלם מקבצים מסוימים
        if self._should_ignore(file_path):
            return
            
        print(f"📝 קובץ שונה: {file_path.name}")
        self._log_change(file_path, "modified")
        self._update_documentation(file_path)
        
    def on_created(self, event):
        """מופעל כשקובץ נוצר"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        if self._should_ignore(file_path):
            return
            
        print(f"✨ קובץ חדש: {file_path.name}")
        self._log_change(file_path, "created")
        self._update_documentation(file_path)
        
    def on_deleted(self, event):
        """מופעל כשקובץ נמחק"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        print(f"🗑️ קובץ נמחק: {file_path.name}")
        self._log_change(file_path, "deleted")
        
    def _should_ignore(self, file_path):
        """בדיקה אם צריך להתעלם מהקובץ"""
        ignore_patterns = [
            '.pyc', '__pycache__', '.git', 'venv', 
            'node_modules', '.env', 'data/storage'
        ]
        return any(pattern in str(file_path) for pattern in ignore_patterns)
        
    def _log_change(self, file_path, change_type):
        """רישום שינוי ב-CHANGES.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        relative_path = file_path.relative_to(self.project_root)
        
        log_entry = f"\n## {timestamp}\n"
        log_entry += f"- **{change_type.upper()}**: `{relative_path}`\n"
        
        # קרא תוכן קיים
        if self.changes_log.exists():
            with open(self.changes_log, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# 📋 יומן שינויים\n\n"
            
        # הוסף שינוי חדש בראש הקובץ
        lines = content.split('\n')
        header = lines[0:2]  # כותרת
        rest = lines[2:]
        
        new_content = '\n'.join(header) + '\n' + log_entry + '\n'.join(rest)
        
        with open(self.changes_log, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    def _update_documentation(self, file_path):
        """עדכון תיעוד לפי סוג הקובץ"""
        if file_path.suffix == '.py':
            self._update_python_docs(file_path)
        elif file_path.suffix in ['.md', '.txt']:
            self._update_content_docs(file_path)
            
    def _update_python_docs(self, file_path):
        """עדכון תיעוד לקובץ Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # חלץ מידע
            functions = self._extract_functions(content)
            classes = self._extract_classes(content)
            
            # עדכן MODULE_INDEX.md
            self._update_module_index(file_path, functions, classes)
            
        except Exception as e:
            print(f"⚠️ שגיאה בעדכון תיעוד: {e}")
            
    def _extract_functions(self, content):
        """חילוץ פונקציות מקוד Python"""
        import re
        pattern = r'def\s+(\w+)\s*\((.*?)\):'
        matches = re.findall(pattern, content)
        return [{"name": name, "params": params} for name, params in matches]
        
    def _extract_classes(self, content):
        """חילוץ מחלקות מקוד Python"""
        import re
        pattern = r'class\s+(\w+)(?:\((.*?)\))?:'
        matches = re.findall(pattern, content)
        return [{"name": name, "base": base} for name, base in matches]
        
    def _update_module_index(self, file_path, functions, classes):
        """עדכון אינדקס מודולים"""
        module_index = self.docs_dir / "MODULE_INDEX.md"
        relative_path = file_path.relative_to(self.project_root)
        
        entry = f"\n### {relative_path}\n"
        entry += f"**עדכון אחרון:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        if classes:
            entry += "**מחלקות:**\n"
            for cls in classes:
                entry += f"- `{cls['name']}`\n"
                
        if functions:
            entry += "\n**פונקציות:**\n"
            for func in functions:
                entry += f"- `{func['name']}({func['params']})`\n"
                
        # קרא או צור קובץ
        if module_index.exists():
            with open(module_index, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# 📚 אינדקס מודולים\n\n"
            
        # הסר ערך ישן אם קיים
        import re
        pattern = f"### {re.escape(str(relative_path))}.*?(?=###|$)"
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # הוסף ערך חדש
        content += entry
        
        with open(module_index, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def _update_content_docs(self, file_path):
        """עדכון תיעוד לקבצי תוכן"""
        pass  # ניתן להוסיף לוגיקה נוספת


def start_monitoring(project_root):
    """התחלת ניטור"""
    print("🔍 מערכת ניטור תיעוד פועלת...")
    print(f"📁 עוקב אחרי: {project_root}")
    print("⏸️ לחץ Ctrl+C לעצירה\n")
    
    event_handler = DocumentationUpdater(project_root)
    observer = Observer()
    observer.schedule(event_handler, project_root, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n✅ ניטור הופסק")
        
    observer.join()


if __name__ == "__main__":
    import sys
    
    # נתיב לפרויקט
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.path.dirname(os.path.abspath(__file__))
        
    start_monitoring(project_root)
