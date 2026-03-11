"""Query router to decide between semantic and structured search"""
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from classification.query_classifier import QueryClassifier, QueryType
from extraction.structured_query import StructuredQueryEngine

class QueryRouter:
    """Routes queries to appropriate engine"""
    
    def __init__(self, structured_data_path: str = "data/extracted_data.json"):
        self.classifier = QueryClassifier()
        self.structured_engine = StructuredQueryEngine(structured_data_path)
        
        # Check if structured data exists
        self.has_structured_data = self.structured_engine.get_stats()["total"] > 0
        
        if self.has_structured_data:
            stats = self.structured_engine.get_stats()
            print(f"Structured data loaded: {stats['total']} items")
            print(f"   - Decisions: {stats['decisions']}")
            print(f"   - Rules: {stats['rules']}")
            print(f"   - Warnings: {stats['warnings']}")
            print(f"   - Changes: {stats['changes']}")
        else:
            print("No structured data found. Run: python scripts/extract_data.py")
    
    def route(self, query: str) -> Dict[str, Any]:
        """
        Route query to appropriate engine
        
        Returns:
            {
                "engine": "semantic" | "structured",
                "classification": {...},
                "structured_results": [...] (if structured)
            }
        """
        
        print(f"[Router] Classifying query: '{query}'")
        
        # Classify query
        classification = self.classifier.classify(query)
        query_type = classification["type"]
        
        print(f"[Router] Classification: {query_type.value}")
        
        # If semantic or no structured data, use semantic
        if query_type == QueryType.SEMANTIC or not self.has_structured_data:
            print(f"[Router] → Routing to SEMANTIC engine")
            return {
                "engine": "semantic",
                "classification": classification,
                "structured_results": None
            }
        
        # Use structured engine
        print(f"[Router] → Routing to STRUCTURED engine")
        print(f"[Router]    Category: {classification['category']}")
        print(f"[Router]    Criteria: {classification.get('filter_criteria')}")
        
        # Map QueryType to query_type string
        type_map = {
            QueryType.STRUCTURED_LIST: "list",
            QueryType.STRUCTURED_FILTER: "filter",
            QueryType.STRUCTURED_LATEST: "latest"
        }
        
        query_type_str = type_map.get(query_type, "list")
        
        # Execute structured query
        results = self.structured_engine.query(
            query_type=query_type_str,
            category=classification["category"],
            filter_criteria=classification.get("filter_criteria")
        )
        
        print(f"[Router] Found {len(results)} results")
        
        return {
            "engine": "structured",
            "classification": classification,
            "structured_results": results
        }
