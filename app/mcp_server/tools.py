from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
import pandas as pd
from app.config import COLLECTION_NAME, EMBEDDING_MODEL

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)


embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def search_milvus(query: str, top_k: int = 5):
    collection = Collection(COLLECTION_NAME)
    collection.load()

    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.search(
        data=query_embedding,
        anns_field="embedding",
        param={"metric_type": "L2"},
        limit=top_k,
        output_fields=["text"]
    )

    contexts = [hit.entity.get("text") for hit in results[0]]

    return {
        "contexts": contexts,
        "tool": "search_milvus"
    }


def read_excel(file_path: str):
    df = pd.read_excel(file_path)
    return {
        "rows": df.head(20).to_dict(),
        "tool": "read_excel"
    }


TOOLS = {
    "search_milvus": {
        "description": "Semantic search over documents using Milvus",
        "params": ["query", "top_k"]
    },
    "read_excel": {
        "description": "Read Excel file and return rows",
        "params": ["file_path"]
    }
}
