from app.ingestion.loaders import (
    load_pdf,
    load_txt,
    load_excel,
    load_docx,
    load_ppt
)
from app.ingestion.chunker import chunk_documents
from app.vector_store.milvus_store import (
    insert_documents,
    reset_collection
)


def ingest_file(file_path: str, filename: str) -> dict:
    """
    Ingest a document into the vector store.

    Steps:
    1. Reset Milvus collection to avoid stale context
    2. Load document based on file type
    3. Chunk document
    4. Insert chunks into Milvus

    Returns:
        dict: ingestion status and number of chunks
    """

    try:
        # 🔥 IMPORTANT: Clear old vectors to avoid mixed retrieval
        reset_collection()

        filename = filename.lower()

        if filename.endswith(".pdf"):
            docs = load_pdf(file_path)

        elif filename.endswith(".txt"):
            docs = load_txt(file_path)

        elif filename.endswith((".csv", ".xlsx")):
            docs = load_excel(file_path)

        elif filename.endswith(".docx"):
            docs = load_docx(file_path)

        elif filename.endswith((".ppt", ".pptx")):
            docs = load_ppt(file_path)

        else:
            raise ValueError(f"Unsupported file type: {filename}")

        # ---- Chunk documents ----
        chunks = chunk_documents(docs)

        if not chunks:
            raise ValueError("No chunks generated from document")

        # ---- Insert into vector store ----
        insert_documents(chunks)

        return {
            "status": "success",
            "chunks_ingested": len(chunks)
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
