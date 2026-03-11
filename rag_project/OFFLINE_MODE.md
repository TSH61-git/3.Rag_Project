# אופציה: Embeddings מקומי (ללא אינטרנט)

## להתקין:
pip install sentence-transformers

## לשנות ב-src/indexer.py:

# במקום:
from llama_index.embeddings.cohere import CohereEmbedding
embed_model = CohereEmbedding(
    api_key=config.COHERE_API_KEY,
    model_name="embed-english-v3.0"
)

# להחליף ל:
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

## יתרונות:
✅ עובד לגמרי offline
✅ אין צורך ב-API key
✅ חינמי לחלוטין

## חסרונות:
❌ איכות נמוכה יותר מ-Cohere
❌ הורדה ראשונית של המודל (~80MB)
