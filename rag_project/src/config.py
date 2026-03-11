import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
STORAGE_DIR = "data/storage"

DOCS_PATHS = {
    "cursor": "mock_docs/cursor",
    "claude_code": "mock_docs/claude_code",
    "task_manager_docs": "mock_docs/task-manager-api/docs"
}

CHUNK_SIZE = 256
CHUNK_OVERLAP = 50
