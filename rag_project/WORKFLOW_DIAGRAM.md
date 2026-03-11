# Event-Driven Workflow - Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query Input                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Validate Input                                      │
│  ────────────────────────────────────────────────────────   │
│  • Check if query is not empty                               │
│  • Check minimum length (3 chars)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ↓ INPUT_VALID                  ↓ INPUT_INVALID
         │                               │
         │                          Return Error
         │                          "Invalid input"
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Retrieve Nodes                                      │
│  ────────────────────────────────────────────────────────   │
│  • Search in vector index                                    │
│  • Get top 3 similar nodes                                   │
│  • Store nodes in State                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┬──────────────┐
         │                               │              │
         ↓ NODES_FOUND                  ↓ NO_NODES     ↓ ERROR
         │                               │              │
         │                          Return Error    Return Error
         │                          "No results"    "System error"
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Check Quality                                       │
│  ────────────────────────────────────────────────────────   │
│  • Calculate average score                                   │
│  • Compare to threshold (0.2)                                │
│  • Store confidence score                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ↓ QUALITY_GOOD                 ↓ QUALITY_LOW
         │                               │
         │                          (Continue anyway)
         │                          (Could add retry logic)
         │
         └───────────────┬───────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Format Response                                     │
│  ────────────────────────────────────────────────────────   │
│  • Build response from nodes                                 │
│  • Add metadata (source, score)                              │
│  • Store in State.response                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓ RESPONSE_READY
                         │
┌─────────────────────────────────────────────────────────────┐
│                    Return Response to User                   │
└─────────────────────────────────────────────────────────────┘
```

## State Management

```python
QueryState {
    query: str              # השאלה המקורית
    nodes: List[Node]       # התוצאות שנמצאו
    confidence_score: float # ציון האמינות
    response: str           # התשובה הסופית
    error: Optional[str]    # שגיאה אם יש
}
```

## Events

- `INPUT_VALID` / `INPUT_INVALID` - תקינות הקלט
- `NODES_FOUND` / `NO_NODES_FOUND` - האם נמצאו תוצאות
- `QUALITY_GOOD` / `QUALITY_LOW` - איכות התוצאות
- `RESPONSE_READY` - התשובה מוכנה
- `ERROR` - שגיאה כללית

## Benefits

✅ כל שלב עצמאי וניתן לבדיקה
✅ קל להוסיף שלבים חדשים
✅ ברור מה קורה בכל נקודה
✅ קל לטפל בשגיאות
✅ ניתן להוסיף retry logic
