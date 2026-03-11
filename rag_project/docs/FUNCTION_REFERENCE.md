# 🔧 מדריך פונקציות

**עדכון אחרון:** 2026-03-11 19:16


### `load_documents()`
**קובץ:** `src\data_loader.py`

Load all markdown documents from configured paths


### `create_index()`
**קובץ:** `src\indexer.py`

Create vector store index from documents

**פרמטרים:**
- `documents`


### `load_existing_index()`
**קובץ:** `src\indexer.py`

Load existing index from disk


### `create_query_engine()`
**קובץ:** `src\query_engine.py`

Create query engine with LLM

**פרמטרים:**
- `index`
- `use_ollama`


### `query()`
**קובץ:** `src\query_engine.py`

Execute query and return response

**פרמטרים:**
- `index_or_engine`
- `question`


### `query()`
**קובץ:** `src\simple_rag.py`

Process query through RAG pipeline

**פרמטרים:**
- `self`
- `question`


### `run()`
**קובץ:** `src\sync_event_workflow.py`

Run the workflow synchronously

**פרמטרים:**
- `self`
- `query`


### `validate_input()`
**קובץ:** `src\sync_event_workflow.py`

Step 1: Validate user input

**פרמטרים:**
- `self`
- `query`
- `state`


### `retrieve_nodes()`
**קובץ:** `src\sync_event_workflow.py`

Step 2: Retrieve relevant nodes

**פרמטרים:**
- `self`
- `event`
- `state`


### `check_quality()`
**קובץ:** `src\sync_event_workflow.py`

Step 3: Check quality and route

**פרמטרים:**
- `self`
- `event`
- `state`


### `synthesize_response()`
**קובץ:** `src\sync_event_workflow.py`

Step 4: Synthesize with LLM

**פרמטרים:**
- `self`
- `event`
- `state`


### `format_response()`
**קובץ:** `src\sync_event_workflow.py`

Step 5: Format final response

**פרמטרים:**
- `self`
- `event`
- `state`


### `run()`
**קובץ:** `src\sync_event_workflow_v2.py`

Run the workflow synchronously

**פרמטרים:**
- `self`
- `query`


### `validate_input()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 1: Validate user input

**פרמטרים:**
- `self`
- `query`
- `state`


### `route_query()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 2: Route query to appropriate engine

**פרמטרים:**
- `self`
- `event`
- `state`


### `synthesize_structured_response()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 3b: Synthesize response from structured data

**פרמטרים:**
- `self`
- `event`
- `state`


### `retrieve_nodes()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 3: Retrieve relevant nodes (semantic path)

**פרמטרים:**
- `self`
- `event`
- `state`


### `check_quality()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 4: Check quality and route (semantic path)

**פרמטרים:**
- `self`
- `event`
- `state`


### `synthesize_response()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 5: Synthesize with LLM (semantic path)

**פרמטרים:**
- `self`
- `event`
- `state`


### `format_response()`
**קובץ:** `src\sync_event_workflow_v2.py`

Step 6: Format final response

**פרמטרים:**
- `self`
- `event`
- `state`


### `execute()`
**קובץ:** `src\workflow_engine.py`

מריץ את כל התהליך מתחילה לסוף

**פרמטרים:**
- `self`
- `query`


### `has_nodes()`
**קובץ:** `src\workflow_models.py`

**פרמטרים:**
- `self`


### `get_avg_score()`
**קובץ:** `src\workflow_models.py`

**פרמטרים:**
- `self`


### `validate_input()`
**קובץ:** `src\workflow_steps.py`

שלב 1: בדיקת תקינות הקלט

**פרמטרים:**
- `state`


### `retrieve_nodes()`
**קובץ:** `src\workflow_steps.py`

שלב 2: חיפוש במסמכים

**פרמטרים:**
- `state`
- `index`


### `check_quality()`
**קובץ:** `src\workflow_steps.py`

שלב 3: בדיקת איכות התוצאות

**פרמטרים:**
- `state`


### `format_response()`
**קובץ:** `src\workflow_steps.py`

שלב 4: עיצוב התשובה

**פרמטרים:**
- `state`


### `classify()`
**קובץ:** `src\classification\query_classifier.py`

Classify a query and return type + metadata

Returns:
    {
        "type": QueryType,
        "category": str (decisions/rules/warnings/changes),
        "filter_criteria": dict (for STRUCTURED_FILTER)
    }

**פרמטרים:**
- `self`
- `query`


### `is_structured_query()`
**קובץ:** `src\classification\query_classifier.py`

Quick check if query needs structured data

**פרמטרים:**
- `self`
- `query`


### `extract_from_file()`
**קובץ:** `src\extraction\extractor.py`

Extract structured data from a single markdown file

**פרמטרים:**
- `self`
- `file_path`
- `tool_name`


### `extract_from_directory()`
**קובץ:** `src\extraction\extractor.py`

Extract from all markdown files in a directory

**פרמטרים:**
- `self`
- `dir_path`
- `tool_name`


### `extract_all()`
**קובץ:** `src\extraction\extractor.py`

Extract from all configured documentation paths

**פרמטרים:**
- `self`
- `docs_paths`


### `save_to_json()`
**קובץ:** `src\extraction\extractor.py`

Save extracted data to JSON file

**פרמטרים:**
- `self`
- `extracted_data`
- `output_path`


### `to_dict()`
**קובץ:** `src\extraction\schema.py`

Convert to dictionary for JSON serialization

**פרמטרים:**
- `self`


### `query()`
**קובץ:** `src\extraction\structured_query.py`

Execute structured query

Args:
    query_type: "list", "filter", "latest"
    category: "decisions", "rules", "warnings", "changes"
    filter_criteria: Optional filters

Returns:
    List of matching items

**פרמטרים:**
- `self`
- `query_type`
- `category`
- `filter_criteria`


### `format_results()`
**קובץ:** `src\extraction\structured_query.py`

Format results for display

**פרמטרים:**
- `self`
- `items`
- `category`


### `get_stats()`
**קובץ:** `src\extraction\structured_query.py`

Get statistics about extracted data

**פרמטרים:**
- `self`


### `get_date()`
**קובץ:** `src\extraction\structured_query.py`

**פרמטרים:**
- `item`


### `route()`
**קובץ:** `src\routing\query_router.py`

Route query to appropriate engine

Returns:
    {
        "engine": "semantic" | "structured",
        "classification": {...},
        "structured_results": [...] (if structured)
    }

**פרמטרים:**
- `self`
- `query`


### `check_and_rebuild_if_needed()`
**קובץ:** `src\utils\sync_manager.py`

פונקציה עזר - בודקת ומבצעת rebuild אם צריך


### `check_changes()`
**קובץ:** `src\utils\sync_manager.py`

בדיקת שינויים בקבצים

Returns:
    Dict עם 'added', 'modified', 'deleted'

**פרמטרים:**
- `self`
- `docs_paths`


### `update_state()`
**קובץ:** `src\utils\sync_manager.py`

עדכון מצב אחרי sync

**פרמטרים:**
- `self`
- `docs_paths`


### `needs_rebuild()`
**קובץ:** `src\utils\sync_manager.py`

האם צריך rebuild?

**פרמטרים:**
- `self`
- `docs_paths`

