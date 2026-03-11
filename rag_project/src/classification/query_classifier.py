"""Query classifier to determine query type"""
from enum import Enum
from typing import Dict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

class QueryType(Enum):
    """Types of queries"""
    SEMANTIC = "semantic"  # Regular semantic search
    STRUCTURED_LIST = "structured_list"  # List all items of a type
    STRUCTURED_FILTER = "structured_filter"  # Filter by criteria
    STRUCTURED_LATEST = "structured_latest"  # Get most recent/current

class QueryClassifier:
    """Classify queries to determine routing"""
    
    def __init__(self):
        from cohere import Client
        self.client = Client(api_key=config.COHERE_API_KEY)
        self.model = "command-r-plus-08-2024"
    
    def classify(self, query: str) -> Dict:
        """
        Classify a query and return type + metadata
        
        Returns:
            {
                "type": QueryType,
                "category": str (decisions/rules/warnings/changes),
                "filter_criteria": dict (for STRUCTURED_FILTER)
            }
        """
        
        prompt = f"""Analyze this user query and classify it.

Query: "{query}"

Determine:
1. Query Type:
   - SEMANTIC: General question that needs semantic search (e.g., "What is the primary color?", "How does authentication work?")
   - STRUCTURED_LIST: Asking for a complete list (e.g., "List all decisions", "Show me all warnings", "What are all the rules?")
   - STRUCTURED_FILTER: Asking for filtered items (e.g., "Decisions from last week", "High severity warnings", "Changes to the database")
   - STRUCTURED_LATEST: Asking for the most recent/current (e.g., "What's the latest rule about RTL?", "Current authentication decision")

2. Category (if structured):
   - decisions: Technical decisions
   - rules: Guidelines and rules
   - warnings: Warnings and sensitive areas
   - changes: Recent changes
   - null: if SEMANTIC

3. Filter Criteria (if STRUCTURED_FILTER):
   - date_range: "last_week", "last_month", "recent", null
   - severity: "high", "critical", "medium", "low", null
   - area: specific area/component, null
   - tags: relevant tags, null

Return ONLY valid JSON:
{{
  "type": "SEMANTIC|STRUCTURED_LIST|STRUCTURED_FILTER|STRUCTURED_LATEST",
  "category": "decisions|rules|warnings|changes|null",
  "filter_criteria": {{
    "date_range": "...",
    "severity": "...",
    "area": "...",
    "tags": [...]
  }}
}}

Examples:
- "What is the primary color?" → {{"type": "SEMANTIC", "category": null, "filter_criteria": null}}
- "List all technical decisions" → {{"type": "STRUCTURED_LIST", "category": "decisions", "filter_criteria": null}}
- "Show me critical warnings" → {{"type": "STRUCTURED_FILTER", "category": "warnings", "filter_criteria": {{"severity": "critical"}}}}
- "What's the latest RTL rule?" → {{"type": "STRUCTURED_LATEST", "category": "rules", "filter_criteria": {{"tags": ["rtl"]}}}}

Return only JSON, no explanation.
"""
        
        try:
            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=0.1
            )
            
            # Parse response
            import json
            response_text = response.text.strip()
            
            # Remove markdown if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            classification = json.loads(response_text.strip())
            
            # Convert type string to enum
            query_type = QueryType(classification["type"].lower())
            
            return {
                "type": query_type,
                "category": classification.get("category"),
                "filter_criteria": classification.get("filter_criteria")
            }
            
        except Exception as e:
            print(f"Classification error: {e}")
            # Default to semantic search
            return {
                "type": QueryType.SEMANTIC,
                "category": None,
                "filter_criteria": None
            }
    
    def is_structured_query(self, query: str) -> bool:
        """Quick check if query needs structured data"""
        classification = self.classify(query)
        return classification["type"] != QueryType.SEMANTIC
