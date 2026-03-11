"""
מחולל תיעוד אוטומטי - סורק את הקוד ומייצר תיעוד
"""
import os
import ast
from pathlib import Path
from datetime import datetime

class DocGenerator:
    """מחולל תיעוד אוטומטי"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.docs_dir = self.project_root / "docs"
        
    def generate_all(self):
        """יצירת כל התיעוד"""
        print("מייצר תיעוד אוטומטי...")
        
        self.generate_module_index()
        self.generate_function_reference()
        self.generate_class_reference()
        
        print("תיעוד נוצר בהצלחה!")
        
    def generate_module_index(self):
        """יצירת אינדקס מודולים"""
        output = "# 📚 אינדקס מודולים\n\n"
        output += f"**עדכון אחרון:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for py_file in self.src_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            relative_path = py_file.relative_to(self.project_root)
            output += f"\n## {relative_path}\n\n"
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    
                # חלץ docstring
                docstring = ast.get_docstring(tree)
                if docstring:
                    output += f"**תיאור:** {docstring.split(chr(10))[0]}\n\n"
                
                # חלץ מחלקות
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                if classes:
                    output += "**מחלקות:**\n"
                    for cls in classes:
                        output += f"- `{cls}`\n"
                    output += "\n"
                
                # חלץ פונקציות
                functions = [node.name for node in ast.walk(tree) 
                           if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')]
                if functions:
                    output += "**פונקציות:**\n"
                    for func in functions:
                        output += f"- `{func}()`\n"
                    output += "\n"
                    
            except Exception as e:
                output += f"⚠️ שגיאה בניתוח: {e}\n\n"
        
        # שמור
        output_file = self.docs_dir / "MODULE_INDEX.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
            
        print(f"נוצר: {output_file}")
        
    def generate_function_reference(self):
        """יצירת מדריך פונקציות"""
        output = "# 🔧 מדריך פונקציות\n\n"
        output += f"**עדכון אחרון:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for py_file in self.src_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        output += f"\n### `{node.name}()`\n"
                        output += f"**קובץ:** `{py_file.relative_to(self.project_root)}`\n\n"
                        
                        # Docstring
                        docstring = ast.get_docstring(node)
                        if docstring:
                            output += f"{docstring}\n\n"
                        
                        # פרמטרים
                        args = [arg.arg for arg in node.args.args]
                        if args:
                            output += "**פרמטרים:**\n"
                            for arg in args:
                                output += f"- `{arg}`\n"
                            output += "\n"
                            
            except Exception as e:
                pass
        
        # שמור
        output_file = self.docs_dir / "FUNCTION_REFERENCE.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
            
        print(f"נוצר: {output_file}")
        
    def generate_class_reference(self):
        """יצירת מדריך מחלקות"""
        output = "# 📦 מדריך מחלקות\n\n"
        output += f"**עדכון אחרון:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for py_file in self.src_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        output += f"\n## `{node.name}`\n"
                        output += f"**קובץ:** `{py_file.relative_to(self.project_root)}`\n\n"
                        
                        # Docstring
                        docstring = ast.get_docstring(node)
                        if docstring:
                            output += f"{docstring}\n\n"
                        
                        # מתודות
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        if methods:
                            output += "**מתודות:**\n"
                            for method in methods:
                                output += f"- `{method}()`\n"
                            output += "\n"
                            
            except Exception as e:
                pass
        
        # שמור
        output_file = self.docs_dir / "CLASS_REFERENCE.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
            
        print(f"נוצר: {output_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    generator = DocGenerator(project_root)
    generator.generate_all()
