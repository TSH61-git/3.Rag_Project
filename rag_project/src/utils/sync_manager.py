"""
Sync Manager - מנהל סינכרון בין קבצי MD לבין האינדקס
כרגע לא בשימוש - מוכן לשימוש עתידי
"""
import os
import json
import hashlib
from typing import Dict, List
from datetime import datetime

class SyncManager:
    """מעקב אחרי שינויים בקבצי MD"""
    
    def __init__(self, state_file: str = "data/sync_state.json"):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """טעינת מצב אחרון"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"files": {}, "last_sync": None}
    
    def _save_state(self):
        """שמירת מצב"""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_file_hash(self, filepath: str) -> str:
        """חישוב hash של קובץ"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def check_changes(self, docs_paths: Dict[str, str]) -> Dict[str, List[str]]:
        """בדיקת שינויים בקבצים
        
        Returns:
            Dict עם 'added', 'modified', 'deleted'
        """
        changes = {
            "added": [],
            "modified": [],
            "deleted": []
        }
        
        current_files = {}
        
        # סריקת כל הקבצים הנוכחיים
        for name, path in docs_paths.items():
            if not os.path.exists(path):
                continue
            
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith('.md'):
                        filepath = os.path.join(root, file)
                        file_hash = self._get_file_hash(filepath)
                        current_files[filepath] = file_hash
                        
                        # בדיקה אם קובץ חדש או שונה
                        if filepath not in self.state["files"]:
                            changes["added"].append(filepath)
                        elif self.state["files"][filepath] != file_hash:
                            changes["modified"].append(filepath)
        
        # בדיקת קבצים שנמחקו
        for filepath in self.state["files"]:
            if filepath not in current_files:
                changes["deleted"].append(filepath)
        
        return changes
    
    def update_state(self, docs_paths: Dict[str, str]):
        """עדכון מצב אחרי sync"""
        current_files = {}
        
        for name, path in docs_paths.items():
            if not os.path.exists(path):
                continue
            
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith('.md'):
                        filepath = os.path.join(root, file)
                        file_hash = self._get_file_hash(filepath)
                        current_files[filepath] = file_hash
        
        self.state["files"] = current_files
        self.state["last_sync"] = datetime.now().isoformat()
        self._save_state()
    
    def needs_rebuild(self, docs_paths: Dict[str, str]) -> bool:
        """האם צריך rebuild?"""
        changes = self.check_changes(docs_paths)
        return bool(changes["added"] or changes["modified"] or changes["deleted"])


def check_and_rebuild_if_needed():
    """פונקציה עזר - בודקת ומבצעת rebuild אם צריך"""
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config import DOCS_PATHS
    
    sync_manager = SyncManager()
    
    if sync_manager.needs_rebuild(DOCS_PATHS):
        changes = sync_manager.check_changes(DOCS_PATHS)
        print(f"זוהו שינויים:")
        print(f"  קבצים חדשים: {len(changes['added'])}")
        print(f"  קבצים ששונו: {len(changes['modified'])}")
        print(f"  קבצים שנמחקו: {len(changes['deleted'])}")
        print("\nמריץ rebuild...")
        
        # הרצת extraction ו-indexing
        import subprocess
        subprocess.run(["python", "extract_data.py"])
        subprocess.run(["python", "build_index.py"])
        
        # עדכון מצב
        sync_manager.update_state(DOCS_PATHS)
        print("Rebuild הושלם!")
        return True
    else:
        print("אין שינויים - לא צריך rebuild")
        return False


if __name__ == "__main__":
    check_and_rebuild_if_needed()
