# 📚 אינדקס מודולים

**עדכון אחרון:** 2026-03-11 19:16


## src\config.py


## src\data_loader.py

**פונקציות:**
- `load_documents()`


## src\indexer.py

**פונקציות:**
- `create_index()`
- `load_existing_index()`


## src\query_engine.py

**פונקציות:**
- `create_query_engine()`
- `query()`


## src\rag_workflow.py

**מחלקות:**
- `InputValidatedEvent`
- `NodesRetrievedEvent`
- `QualityCheckedEvent`
- `NeedMoreContextEvent`
- `ResponseSynthesizedEvent`
- `RAGWorkflow`


## src\simple_rag.py

**תיאור:** Simple synchronous RAG pipeline

**מחלקות:**
- `SimpleRAGPipeline`

**פונקציות:**
- `query()`


## src\sync_event_workflow.py

**תיאור:** Synchronous Event-Driven RAG Workflow

**מחלקות:**
- `InputValidatedEvent`
- `NodesRetrievedEvent`
- `QualityCheckedEvent`
- `NeedMoreContextEvent`
- `ResponseSynthesizedEvent`
- `StopEvent`
- `WorkflowState`
- `SyncRAGWorkflow`

**פונקציות:**
- `run()`
- `validate_input()`
- `retrieve_nodes()`
- `check_quality()`
- `synthesize_response()`
- `format_response()`


## src\sync_event_workflow_v2.py

**תיאור:** Synchronous Event-Driven RAG Workflow with Routing

**מחלקות:**
- `InputValidatedEvent`
- `QueryRoutedEvent`
- `NodesRetrievedEvent`
- `QualityCheckedEvent`
- `NeedMoreContextEvent`
- `ResponseSynthesizedEvent`
- `StopEvent`
- `WorkflowState`
- `SyncRAGWorkflow`

**פונקציות:**
- `run()`
- `validate_input()`
- `route_query()`
- `synthesize_structured_response()`
- `retrieve_nodes()`
- `check_quality()`
- `synthesize_response()`
- `format_response()`


## src\workflow_engine.py

**מחלקות:**
- `WorkflowEngine`

**פונקציות:**
- `execute()`


## src\workflow_models.py

**מחלקות:**
- `EventType`
- `Event`
- `QueryState`

**פונקציות:**
- `has_nodes()`
- `get_avg_score()`


## src\workflow_steps.py

**מחלקות:**
- `WorkflowSteps`

**פונקציות:**
- `validate_input()`
- `retrieve_nodes()`
- `check_quality()`
- `format_response()`


## src\classification\query_classifier.py

**תיאור:** Query classifier to determine query type

**מחלקות:**
- `QueryType`
- `QueryClassifier`

**פונקציות:**
- `classify()`
- `is_structured_query()`


## src\extraction\extractor.py

**תיאור:** Data extractor using LLM to extract structured information from markdown files

**מחלקות:**
- `DataExtractor`

**פונקציות:**
- `extract_from_file()`
- `extract_from_directory()`
- `extract_all()`
- `save_to_json()`


## src\extraction\schema.py

**תיאור:** Schema definitions for structured data extraction

**מחלקות:**
- `SourceInfo`
- `Decision`
- `Rule`
- `Warning`
- `Change`
- `FileSource`
- `ToolSource`
- `ExtractedData`

**פונקציות:**
- `to_dict()`


## src\extraction\structured_query.py

**תיאור:** Structured query engine for extracted data

**מחלקות:**
- `StructuredQueryEngine`

**פונקציות:**
- `query()`
- `format_results()`
- `get_stats()`
- `get_date()`


## src\routing\query_router.py

**תיאור:** Query router to decide between semantic and structured search

**מחלקות:**
- `QueryRouter`

**פונקציות:**
- `route()`


## src\utils\sync_manager.py

**תיאור:** Sync Manager - מנהל סינכרון בין קבצי MD לבין האינדקס

**מחלקות:**
- `SyncManager`

**פונקציות:**
- `check_and_rebuild_if_needed()`
- `check_changes()`
- `update_state()`
- `needs_rebuild()`


## src\utils\__init__.py

