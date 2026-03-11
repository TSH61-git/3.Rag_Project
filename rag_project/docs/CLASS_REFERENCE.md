# 📦 מדריך מחלקות

**עדכון אחרון:** 2026-03-11 19:16


## `InputValidatedEvent`
**קובץ:** `src\rag_workflow.py`


## `NodesRetrievedEvent`
**קובץ:** `src\rag_workflow.py`


## `QualityCheckedEvent`
**קובץ:** `src\rag_workflow.py`


## `NeedMoreContextEvent`
**קובץ:** `src\rag_workflow.py`


## `ResponseSynthesizedEvent`
**קובץ:** `src\rag_workflow.py`


## `RAGWorkflow`
**קובץ:** `src\rag_workflow.py`

Event-Driven RAG Workflow with validations and routing

**מתודות:**
- `__init__()`


## `SimpleRAGPipeline`
**קובץ:** `src\simple_rag.py`

Simple RAG pipeline without async complexity

**מתודות:**
- `__init__()`
- `query()`


## `InputValidatedEvent`
**קובץ:** `src\sync_event_workflow.py`


## `NodesRetrievedEvent`
**קובץ:** `src\sync_event_workflow.py`


## `QualityCheckedEvent`
**קובץ:** `src\sync_event_workflow.py`


## `NeedMoreContextEvent`
**קובץ:** `src\sync_event_workflow.py`


## `ResponseSynthesizedEvent`
**קובץ:** `src\sync_event_workflow.py`


## `StopEvent`
**קובץ:** `src\sync_event_workflow.py`


## `WorkflowState`
**קובץ:** `src\sync_event_workflow.py`

**מתודות:**
- `__init__()`


## `SyncRAGWorkflow`
**קובץ:** `src\sync_event_workflow.py`

Event-Driven RAG without async complexity

**מתודות:**
- `__init__()`
- `run()`
- `validate_input()`
- `retrieve_nodes()`
- `check_quality()`
- `synthesize_response()`
- `format_response()`


## `InputValidatedEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `QueryRoutedEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `NodesRetrievedEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `QualityCheckedEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `NeedMoreContextEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `ResponseSynthesizedEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `StopEvent`
**קובץ:** `src\sync_event_workflow_v2.py`


## `WorkflowState`
**קובץ:** `src\sync_event_workflow_v2.py`

**מתודות:**
- `__init__()`


## `SyncRAGWorkflow`
**קובץ:** `src\sync_event_workflow_v2.py`

Event-Driven RAG with Routing

**מתודות:**
- `__init__()`
- `run()`
- `validate_input()`
- `route_query()`
- `synthesize_structured_response()`
- `retrieve_nodes()`
- `check_quality()`
- `synthesize_response()`
- `format_response()`


## `WorkflowEngine`
**קובץ:** `src\workflow_engine.py`

המנוע שמריץ את כל התהליך

**מתודות:**
- `__init__()`
- `execute()`
- `_handle_invalid_input()`
- `_handle_no_results()`
- `_handle_error()`


## `EventType`
**קובץ:** `src\workflow_models.py`


## `Event`
**קובץ:** `src\workflow_models.py`

אירוע שקורה בזרימה


## `QueryState`
**קובץ:** `src\workflow_models.py`

מצב השאילתה לאורך כל התהליך

**מתודות:**
- `has_nodes()`
- `get_avg_score()`


## `WorkflowSteps`
**קובץ:** `src\workflow_steps.py`

כל השלבים בתהליך השאילתה

**מתודות:**
- `validate_input()`
- `retrieve_nodes()`
- `check_quality()`
- `format_response()`


## `QueryType`
**קובץ:** `src\classification\query_classifier.py`

Types of queries


## `QueryClassifier`
**קובץ:** `src\classification\query_classifier.py`

Classify queries to determine routing

**מתודות:**
- `__init__()`
- `classify()`
- `is_structured_query()`


## `DataExtractor`
**קובץ:** `src\extraction\extractor.py`

Extract structured data from markdown files using LLM

**מתודות:**
- `__init__()`
- `extract_from_file()`
- `extract_from_directory()`
- `extract_all()`
- `_hash_file()`
- `save_to_json()`


## `SourceInfo`
**קובץ:** `src\extraction\schema.py`

Information about where the data came from


## `Decision`
**קובץ:** `src\extraction\schema.py`

Technical decision


## `Rule`
**קובץ:** `src\extraction\schema.py`

Guideline or rule


## `Warning`
**קובץ:** `src\extraction\schema.py`

Warning or sensitive area


## `Change`
**קובץ:** `src\extraction\schema.py`

Recent change or update


## `FileSource`
**קובץ:** `src\extraction\schema.py`

Information about a source file


## `ToolSource`
**קובץ:** `src\extraction\schema.py`

Information about a tool's documentation


## `ExtractedData`
**קובץ:** `src\extraction\schema.py`

Complete extracted data structure

**מתודות:**
- `to_dict()`
- `_decision_to_dict()`
- `_rule_to_dict()`
- `_warning_to_dict()`
- `_change_to_dict()`
- `_source_to_dict()`


## `StructuredQueryEngine`
**קובץ:** `src\extraction\structured_query.py`

Query engine for structured extracted data

**מתודות:**
- `__init__()`
- `_load_data()`
- `query()`
- `_list_all()`
- `_filter_items()`
- `_filter_by_date()`
- `_get_latest()`
- `format_results()`
- `get_stats()`


## `QueryRouter`
**קובץ:** `src\routing\query_router.py`

Routes queries to appropriate engine

**מתודות:**
- `__init__()`
- `route()`


## `SyncManager`
**קובץ:** `src\utils\sync_manager.py`

מעקב אחרי שינויים בקבצי MD

**מתודות:**
- `__init__()`
- `_load_state()`
- `_save_state()`
- `_get_file_hash()`
- `check_changes()`
- `update_state()`
- `needs_rebuild()`

