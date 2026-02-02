Agentic RAG System with MCP, Milvus & Ollama

An enterprise-ready Agentic Retrieval-Augmented Generation (RAG) system that uses multiple AI agents to intelligently retrieve, reason, and answer questions from documents using self-hosted LLMs.

🚀 Features

1. Planner Agent – decides retrieval strategy

2. Execution Agent – calls MCP tools (Milvus, Excel, PDF)

3. Generator Agent – answers using Ollama (local LLM)

4. Critic Agent – validates grounding & prevents hallucinations

5. Supports PDF, TXT, CSV, Excel, DOCX, PPT

6. Milvus vector database

7. MCP (Model Context Protocol) server

🖥️ Clean Streamlit UI

Self-hosted

Architecture
 
User
 ↓
Streamlit UI
 ↓
Planner Agent
 ↓
Execution Agent (MCP Client)
 ↓
MCP Server
 ↓
Milvus Vector DB
 ↓
Generator Agent (Ollama)
 ↓
Critic Agent
 ↓
Final Answer


🧩 Tech Stack

Python

Milvus (Vector DB)

Ollama (Self-hosted LLM)

MCP Server

LangChain

Streamlit

Docker

⚙️ Setup Instructions
1️. Start Milvus
docker compose -f docker/milvus.yml up -d

2️. Start MCP Server
uvicorn app.mcp_server.server:app --port 8001

3️. Start Streamlit UI
streamlit run app/ui/streamlit_app.py --server.fileWatcherType none

Key Design Decisions

Agentic orchestration instead of monolithic RAG

Critic agent to reduce hallucinations

Reset vector store per ingestion for clean grounding
