"""Data extractor using LLM to extract structured information from markdown files"""
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import config
from extraction.schema import (
    ExtractedData, Decision, Rule, Warning, Change,
    SourceInfo, FileSource, ToolSource,
    EXTRACTION_PROMPT
)

class DataExtractor:
    """Extract structured data from markdown files using LLM"""
    
    def __init__(self):
        from cohere import Client
        self.client = Client(api_key=config.COHERE_API_KEY)
        self.model = "command-r-plus-08-2024"
    
    def extract_from_file(self, file_path: str, tool_name: str) -> Dict[str, List[Dict]]:
        """Extract structured data from a single markdown file"""
        print(f"  Extracting from: {os.path.basename(file_path)}")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"    ❌ Error reading file: {e}")
            return {"decisions": [], "rules": [], "warnings": [], "changes": []}
        
        # Skip if file is too short
        if len(content.strip()) < 100:
            print(f"    ⚠️ File too short, skipping")
            return {"decisions": [], "rules": [], "warnings": [], "changes": []}
        
        # Create prompt
        prompt = EXTRACTION_PROMPT.format(content=content)
        
        # Call LLM
        try:
            print(f"    🤖 Calling LLM...")
            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=0.1  # Low temperature for consistent extraction
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            extracted = json.loads(response_text.strip())
            
            # Add source info to each item
            source_info = {
                "tool": tool_name,
                "file": file_path,
                "anchor": None,
                "line_range": None
            }
            
            for category in ["decisions", "rules", "warnings", "changes"]:
                for item in extracted.get(category, []):
                    item["source"] = source_info
                    item["observed_at"] = datetime.now().isoformat()
            
            counts = {k: len(v) for k, v in extracted.items()}
            print(f"    ✅ Extracted: {counts}")
            
            return extracted
            
        except json.JSONDecodeError as e:
            print(f"    ❌ JSON parsing error: {e}")
            print(f"    Response was: {response_text[:200]}...")
            return {"decisions": [], "rules": [], "warnings": [], "changes": []}
        except Exception as e:
            print(f"    ❌ LLM error: {str(e)[:100]}")
            return {"decisions": [], "rules": [], "warnings": [], "changes": []}
    
    def extract_from_directory(self, dir_path: str, tool_name: str) -> Dict[str, List[Dict]]:
        """Extract from all markdown files in a directory"""
        print(f"\n📂 Processing {tool_name} directory: {dir_path}")
        
        all_extracted = {
            "decisions": [],
            "rules": [],
            "warnings": [],
            "changes": []
        }
        
        # Find all .md files
        md_files = list(Path(dir_path).rglob("*.md"))
        
        if not md_files:
            print(f"  ⚠️ No markdown files found")
            return all_extracted
        
        print(f"  Found {len(md_files)} markdown files")
        
        # Process each file
        for md_file in md_files:
            file_extracted = self.extract_from_file(str(md_file), tool_name)
            
            # Merge results
            for category in all_extracted.keys():
                all_extracted[category].extend(file_extracted.get(category, []))
        
        # Print summary
        total = sum(len(v) for v in all_extracted.values())
        print(f"  ✅ Total extracted from {tool_name}: {total} items")
        for category, items in all_extracted.items():
            if items:
                print(f"     - {category}: {len(items)}")
        
        return all_extracted
    
    def extract_all(self, docs_paths: Dict[str, str]) -> ExtractedData:
        """Extract from all configured documentation paths"""
        print("\n" + "="*60)
        print("🚀 Starting Data Extraction")
        print("="*60)
        
        extracted_data = ExtractedData(
            schema_version="1.0",
            generated_at=datetime.now().isoformat()
        )
        
        # Process each tool's documentation
        for tool_name, dir_path in docs_paths.items():
            if not os.path.exists(dir_path):
                print(f"\n⚠️ Directory not found: {dir_path}")
                continue
            
            # Extract from directory
            tool_extracted = self.extract_from_directory(dir_path, tool_name)
            
            # Add to main data structure
            for category in ["decisions", "rules", "warnings", "changes"]:
                items = tool_extracted.get(category, [])
                for i, item in enumerate(items):
                    # Generate unique ID
                    item_id = f"{category[:3]}-{tool_name[:3]}-{i+1:03d}"
                    item["id"] = item_id
                    
                    # Create appropriate object
                    if category == "decisions":
                        extracted_data.decisions.append(Decision(**item))
                    elif category == "rules":
                        extracted_data.rules.append(Rule(**item))
                    elif category == "warnings":
                        extracted_data.warnings.append(Warning(**item))
                    elif category == "changes":
                        extracted_data.changes.append(Change(**item))
            
            # Add source info
            tool_source = ToolSource(
                tool=tool_name,
                root_path=dir_path,
                files=[]
            )
            
            # Add file info
            for md_file in Path(dir_path).rglob("*.md"):
                file_stat = os.stat(md_file)
                file_source = FileSource(
                    path=str(md_file),
                    last_modified=datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                    hash=self._hash_file(md_file)
                )
                tool_source.files.append(file_source)
            
            extracted_data.sources.append(tool_source)
        
        # Print final summary
        print("\n" + "="*60)
        print("✅ Extraction Complete")
        print("="*60)
        print(f"Total items extracted:")
        print(f"  - Decisions: {len(extracted_data.decisions)}")
        print(f"  - Rules: {len(extracted_data.rules)}")
        print(f"  - Warnings: {len(extracted_data.warnings)}")
        print(f"  - Changes: {len(extracted_data.changes)}")
        print(f"  - TOTAL: {len(extracted_data.decisions) + len(extracted_data.rules) + len(extracted_data.warnings) + len(extracted_data.changes)}")
        print("="*60 + "\n")
        
        return extracted_data
    
    def _hash_file(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return f"sha256:{sha256.hexdigest()[:16]}"
    
    def save_to_json(self, extracted_data: ExtractedData, output_path: str):
        """Save extracted data to JSON file"""
        print(f"💾 Saving to: {output_path}")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert to dict and save
        data_dict = extracted_data.to_dict()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved successfully!")
