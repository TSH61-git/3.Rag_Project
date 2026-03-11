"""Structured query engine for extracted data"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

class StructuredQueryEngine:
    """Query engine for structured extracted data"""
    
    def __init__(self, data_path: str = "data/extracted_data.json"):
        """Initialize with path to extracted data"""
        self.data_path = data_path
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load extracted data from JSON"""
        if not os.path.exists(self.data_path):
            print(f"Extracted data not found at {self.data_path}")
            print("   Run: python scripts/extract_data.py")
            return {"items": {"decisions": [], "rules": [], "warnings": [], "changes": []}}
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def query(self, query_type: str, category: str, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Execute structured query
        
        Args:
            query_type: "list", "filter", "latest"
            category: "decisions", "rules", "warnings", "changes"
            filter_criteria: Optional filters
        
        Returns:
            List of matching items
        """
        
        # Get items of category
        items = self.data.get("items", {}).get(category, [])
        
        if not items:
            return []
        
        # Apply query type
        if query_type == "list":
            return self._list_all(items)
        
        elif query_type == "filter":
            return self._filter_items(items, filter_criteria or {})
        
        elif query_type == "latest":
            return self._get_latest(items, filter_criteria or {})
        
        return []
    
    def _list_all(self, items: List[Dict]) -> List[Dict]:
        """Return all items"""
        return items
    
    def _filter_items(self, items: List[Dict], criteria: Dict) -> List[Dict]:
        """Filter items by criteria"""
        filtered = items
        
        # Filter by date range
        if criteria.get("date_range"):
            filtered = self._filter_by_date(filtered, criteria["date_range"])
        
        # Filter by severity (for warnings)
        if criteria.get("severity"):
            filtered = [item for item in filtered 
                       if item.get("severity") == criteria["severity"]]
        
        # Filter by area
        if criteria.get("area"):
            area_lower = criteria["area"].lower()
            filtered = [item for item in filtered 
                       if area_lower in item.get("area", "").lower() or
                          area_lower in item.get("title", "").lower() or
                          area_lower in item.get("summary", "").lower()]
        
        # Filter by tags
        if criteria.get("tags"):
            search_tags = [t.lower() for t in criteria["tags"]]
            filtered = [item for item in filtered 
                       if any(tag.lower() in search_tags 
                             for tag in item.get("tags", []))]
        
        return filtered
    
    def _filter_by_date(self, items: List[Dict], date_range: str) -> List[Dict]:
        """Filter items by date range"""
        now = datetime.now()
        
        if date_range == "last_week":
            cutoff = now - timedelta(days=7)
        elif date_range == "last_month":
            cutoff = now - timedelta(days=30)
        elif date_range == "recent":
            cutoff = now - timedelta(days=14)
        else:
            return items
        
        filtered = []
        for item in items:
            # Check date field (for decisions, changes)
            date_str = item.get("date") or item.get("last_modified")
            if date_str:
                try:
                    item_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    if item_date >= cutoff:
                        filtered.append(item)
                except:
                    pass
            
            # Check observed_at as fallback
            elif item.get("observed_at"):
                try:
                    observed = datetime.fromisoformat(item["observed_at"].replace("Z", "+00:00"))
                    if observed >= cutoff:
                        filtered.append(item)
                except:
                    pass
        
        return filtered
    
    def _get_latest(self, items: List[Dict], criteria: Dict) -> List[Dict]:
        """Get the most recent item(s)"""
        
        # First filter by criteria if provided
        if criteria:
            items = self._filter_items(items, criteria)
        
        if not items:
            return []
        
        # Sort by date (newest first)
        def get_date(item):
            date_str = item.get("date") or item.get("last_modified") or item.get("observed_at")
            if date_str:
                try:
                    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except:
                    pass
            return datetime.min
        
        sorted_items = sorted(items, key=get_date, reverse=True)
        
        # Return top 3 most recent
        return sorted_items[:3]
    
    def format_results(self, items: List[Dict], category: str) -> str:
        """Format results for display"""
        if not items:
            return "No items found matching your criteria."
        
        result_parts = [f"Found {len(items)} {category}:\n"]
        
        for i, item in enumerate(items, 1):
            result_parts.append(f"\n{i}. **{item.get('title') or item.get('rule') or item.get('area') or item.get('description', 'Item')}**")
            
            # Add relevant fields based on category
            if category == "decisions":
                if item.get("summary"):
                    result_parts.append(f"   Summary: {item['summary']}")
                if item.get("date"):
                    result_parts.append(f"   Date: {item['date']}")
                if item.get("status"):
                    result_parts.append(f"   Status: {item['status']}")
                if item.get("tags"):
                    result_parts.append(f"   Tags: {', '.join(item['tags'])}")
            
            elif category == "rules":
                if item.get("rule"):
                    result_parts.append(f"   Rule: {item['rule']}")
                if item.get("scope"):
                    result_parts.append(f"   Scope: {item['scope']}")
                if item.get("exceptions"):
                    result_parts.append(f"   Exceptions: {item['exceptions']}")
            
            elif category == "warnings":
                if item.get("message"):
                    result_parts.append(f"   Message: {item['message']}")
                if item.get("severity"):
                    result_parts.append(f"   Severity: {item['severity'].upper()}")
                if item.get("last_modified"):
                    result_parts.append(f"   Last Modified: {item['last_modified']}")
            
            elif category == "changes":
                if item.get("description"):
                    result_parts.append(f"   Description: {item['description']}")
                if item.get("type"):
                    result_parts.append(f"   Type: {item['type']}")
                if item.get("date"):
                    result_parts.append(f"   Date: {item['date']}")
                if item.get("impact"):
                    result_parts.append(f"   Impact: {item['impact']}")
            
            # Add source
            if item.get("source"):
                source = item["source"]
                file_name = os.path.basename(source.get("file", ""))
                result_parts.append(f"   Source: {source.get('tool')}/{file_name}")
        
        return "\n".join(result_parts)
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about extracted data"""
        items = self.data.get("items", {})
        return {
            "decisions": len(items.get("decisions", [])),
            "rules": len(items.get("rules", [])),
            "warnings": len(items.get("warnings", [])),
            "changes": len(items.get("changes", [])),
            "total": sum(len(v) for v in items.values())
        }
