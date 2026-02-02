from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader
)
from langchain_core.documents import Document
import pandas as pd


def load_pdf(path):
    docs = PyPDFLoader(path).load()
    for d in docs:
        d.metadata["type"] = "pdf"
    return docs


def load_txt(path):
    docs = TextLoader(path).load()
    for d in docs:
        d.metadata["type"] = "txt"
    return docs


def load_excel(path):
    df = pd.read_excel(path)
    text = df.to_string(index=False)
    return [
        Document(
            page_content=text,
            metadata={"source": path, "type": "excel"}
        )
    ]


def load_docx(path):
    docs = Docx2txtLoader(path).load()
    for d in docs:
        d.metadata["type"] = "docx"
    return docs


def load_ppt(path):
    docs = UnstructuredPowerPointLoader(path).load()
    for d in docs:
        d.metadata["type"] = "ppt"
    return docs
