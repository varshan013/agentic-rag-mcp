from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)
from sentence_transformers import SentenceTransformer
from app.config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, EMBEDDING_MODEL

# ------------------ Connection ------------------
connections.connect(
    alias="default",
    host=MILVUS_HOST,
    port=MILVUS_PORT
)

# ------------------ Embedding Model ------------------
model = SentenceTransformer(EMBEDDING_MODEL)
DIMENSION = 384  # all-MiniLM-L6-v2

# ------------------ Collection Utils ------------------
def reset_collection():
    """
    Drops existing collection to avoid stale / mixed context.
    Called before fresh ingestion.
    """
    if utility.has_collection(COLLECTION_NAME):
        utility.drop_collection(COLLECTION_NAME)


def create_collection():
    """
    Create collection if it does not exist.
    """
    if utility.has_collection(COLLECTION_NAME):
        return Collection(COLLECTION_NAME)

    fields = [
        FieldSchema(
            name="id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True
        ),
        FieldSchema(
            name="embedding",
            dtype=DataType.FLOAT_VECTOR,
            dim=DIMENSION
        ),
        FieldSchema(
            name="text",
            dtype=DataType.VARCHAR,
            max_length=65535
        ),
    ]

    schema = CollectionSchema(
        fields=fields,
        description="Agentic RAG document chunks"
    )

    collection = Collection(
        name=COLLECTION_NAME,
        schema=schema
    )

    return collection


def create_index(collection):
    """
    Create vector index (only once).
    """
    if collection.has_index():
        return

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }

    collection.create_index(
        field_name="embedding",
        index_params=index_params
    )


# ------------------ Insert Documents ------------------
def insert_documents(chunks):
    """
    Insert chunked documents into Milvus.
    """
    collection = create_collection()

    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=False).tolist()

    collection.insert([
        embeddings,
        texts
    ])

    create_index(collection)
    collection.load()
