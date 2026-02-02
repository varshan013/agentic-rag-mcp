from fastapi import FastAPI
from pydantic import BaseModel
from app.mcp_server.tools import search_milvus, read_excel, TOOLS

app = FastAPI(title="MCP Server")


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class ExcelRequest(BaseModel):
    file_path: str


@app.get("/list_tools")
def list_tools():
    return TOOLS


@app.post("/tool/search_milvus")
def run_search(req: SearchRequest):
    return search_milvus(req.query, req.top_k)


@app.post("/tool/read_excel")
def run_excel(req: ExcelRequest):
    return read_excel(req.file_path)
