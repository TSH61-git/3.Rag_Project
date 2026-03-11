"""Schema definitions for structured data extraction"""
from dataclasses import dataclass, field
from typing import List, Optional, Literal
from datetime import datetime

@dataclass
class SourceInfo:
    """Information about where the data came from"""
    tool: str  # cursor, claude_code, etc.
    file: str  # full path to file
    anchor: Optional[str] = None  # section/heading
    line_range: Optional[List[int]] = None  # [start, end]

@dataclass
class Decision:
    """Technical decision"""
    id: str
    title: str
    summary: str
    date: Optional[str] = None  # YYYY-MM-DD
    status: Optional[str] = None  # approved, pending, rejected
    reasoning: Optional[str] = None
    alternatives: Optional[str] = None
    impact: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    source: Optional[SourceInfo] = None
    observed_at: Optional[str] = None  # ISO 8601

@dataclass
class Rule:
    """Guideline or rule"""
    id: str
    rule: str
    scope: str  # ui, api, db, etc.
    exceptions: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    source: Optional[SourceInfo] = None
    observed_at: Optional[str] = None

@dataclass
class Warning:
    """Warning or sensitive area"""
    id: str
    area: str  # authentication, payment, etc.
    message: str
    severity: Literal["low", "medium", "high", "critical"]
    last_modified: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    source: Optional[SourceInfo] = None
    observed_at: Optional[str] = None

@dataclass
class Change:
    """Recent change or update"""
    id: str
    type: str  # schema, api, ui, config, etc.
    description: str
    date: Optional[str] = None
    impact: Optional[str] = None
    related_to: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    source: Optional[SourceInfo] = None
    observed_at: Optional[str] = None

@dataclass
class FileSource:
    """Information about a source file"""
    path: str
    last_modified: Optional[str] = None
    hash: Optional[str] = None

@dataclass
class ToolSource:
    """Information about a tool's documentation"""
    tool: str
    root_path: str
    files: List[FileSource] = field(default_factory=list)

@dataclass
class ExtractedData:
    """Complete extracted data structure"""
    schema_version: str = "1.0"
    generated_at: Optional[str] = None
    sources: List[ToolSource] = field(default_factory=list)
    decisions: List[Decision] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    warnings: List[Warning] = field(default_factory=list)
    changes: List[Change] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "sources": [
                {
                    "tool": src.tool,
                    "root_path": src.root_path,
                    "files": [
                        {
                            "path": f.path,
                            "last_modified": f.last_modified,
                            "hash": f.hash
                        } for f in src.files
                    ]
                } for src in self.sources
            ],
            "items": {
                "decisions": [self._decision_to_dict(d) for d in self.decisions],
                "rules": [self._rule_to_dict(r) for r in self.rules],
                "warnings": [self._warning_to_dict(w) for w in self.warnings],
                "changes": [self._change_to_dict(c) for c in self.changes]
            }
        }
    
    def _decision_to_dict(self, d: Decision):
        return {
            "id": d.id,
            "title": d.title,
            "summary": d.summary,
            "date": d.date,
            "status": d.status,
            "reasoning": d.reasoning,
            "alternatives": d.alternatives,
            "impact": d.impact,
            "tags": d.tags,
            "source": self._source_to_dict(d.source) if d.source else None,
            "observed_at": d.observed_at
        }
    
    def _rule_to_dict(self, r: Rule):
        return {
            "id": r.id,
            "rule": r.rule,
            "scope": r.scope,
            "exceptions": r.exceptions,
            "notes": r.notes,
            "tags": r.tags,
            "source": self._source_to_dict(r.source) if r.source else None,
            "observed_at": r.observed_at
        }
    
    def _warning_to_dict(self, w: Warning):
        return {
            "id": w.id,
            "area": w.area,
            "message": w.message,
            "severity": w.severity,
            "last_modified": w.last_modified,
            "tags": w.tags,
            "source": self._source_to_dict(w.source) if w.source else None,
            "observed_at": w.observed_at
        }
    
    def _change_to_dict(self, c: Change):
        return {
            "id": c.id,
            "type": c.type,
            "description": c.description,
            "date": c.date,
            "impact": c.impact,
            "related_to": c.related_to,
            "tags": c.tags,
            "source": self._source_to_dict(c.source) if c.source else None,
            "observed_at": c.observed_at
        }
    
    def _source_to_dict(self, s):  
        if isinstance(s, dict):
            return s
        return {
            "tool": s.tool,
            "file": s.file,
            "anchor": s.anchor,
            "line_range": s.line_range
        }


# Extraction prompt template
EXTRACTION_PROMPT = """Extract structured information from the following documentation file.

Extract these categories:

1. **Decisions** - Technical decisions with:
   - Title (short name)
   - Summary (what was decided)
   - Date (if mentioned)
   - Status (approved/pending/rejected if mentioned)
   - Reasoning (why this decision)
   - Alternatives (other options considered)
   - Impact (what this affects)
   - Tags (relevant keywords)

2. **Rules** - Guidelines and rules with:
   - Rule (the actual rule/guideline)
   - Scope (where it applies: ui/api/db/etc)
   - Exceptions (if any)
   - Notes (additional context)
   - Tags (relevant keywords)

3. **Warnings** - Sensitive areas or warnings with:
   - Area (what component/module)
   - Message (the warning text)
   - Severity (low/medium/high/critical)
   - Last modified date (if mentioned)
   - Tags (relevant keywords)

4. **Changes** - Recent changes or updates with:
   - Type (schema/api/ui/config/etc)
   - Description (what changed)
   - Date (when it changed)
   - Impact (what's affected)
   - Related to (related component)
   - Tags (relevant keywords)

Return ONLY valid JSON in this exact format:
{{
  "decisions": [
    {{
      "title": "...",
      "summary": "...",
      "date": "YYYY-MM-DD or null",
      "status": "approved/pending/rejected or null",
      "reasoning": "...",
      "alternatives": "...",
      "impact": "...",
      "tags": ["tag1", "tag2"]
    }}
  ],
  "rules": [
    {{
      "rule": "...",
      "scope": "ui/api/db/etc",
      "exceptions": "...",
      "notes": "...",
      "tags": ["tag1", "tag2"]
    }}
  ],
  "warnings": [
    {{
      "area": "...",
      "message": "...",
      "severity": "low/medium/high/critical",
      "last_modified": "YYYY-MM-DD or null",
      "tags": ["tag1", "tag2"]
    }}
  ],
  "changes": [
    {{
      "type": "schema/api/ui/config/etc",
      "description": "...",
      "date": "YYYY-MM-DD or null",
      "impact": "...",
      "related_to": "...",
      "tags": ["tag1", "tag2"]
    }}
  ]
}}

If a category has no items, return an empty array [].

Documentation file content:
---
{content}
---

Return only the JSON, no additional text.
"""
