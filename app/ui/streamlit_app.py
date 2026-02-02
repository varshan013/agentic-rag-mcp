# Streamlit App – Agentic RAG UI

import streamlit as st

st.set_page_config(
    page_title="Agentic RAG System",
    page_icon="🤖",
    layout="centered"
)

import sys
import os
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(PROJECT_ROOT)

from app.ingest import ingest_file
from app.agents.planner_agent import PlannerAgent
from app.agents.execution_agent import ExecutionAgent
from app.agents.generator_agent import GeneratorAgent
from app.agents.critic_agent import CriticAgent


st.title("🤖 Agentic RAG System")
st.caption("Planner → Execution → Generator → Critic")


st.subheader("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF, TXT, CSV,PPT or Excel file",
    type=["pdf", "txt", "csv", "xlsx", "docx", "ppt", "pptx"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    if st.button("Ingest Document"):
        with st.spinner("Ingesting document into vector store..."):
            ingest_file(temp_path, uploaded_file.name)
            st.success("✅ Document ingested successfully!")


planner = PlannerAgent()
executor = ExecutionAgent()
generator = GeneratorAgent()
critic = CriticAgent()


st.subheader("💬 Ask a Question")

user_query = st.text_input(
    "Enter your question:",
    placeholder="e.g. What is the document about?"
)

if st.button("Run Agentic RAG") and user_query:
    with st.spinner("Running agentic pipeline..."):

        # ---- Step 1: Planning ----
        st.subheader("🧠 Planner")
        plan = planner.plan(user_query)
        st.code(plan, language="json")

        # ---- Step 2: Execution ----
        st.subheader("🔍 Execution (MCP Tools)")
        execution_result = executor.execute(plan, user_query)
        st.success("Context retrieved")

        # ---- Step 3: Generation ----
        st.subheader("✍️ Generator (Ollama)")
        answer = generator.generate(user_query, execution_result)
        st.text_area("Generated Answer", answer, height=220)

        # ---- Step 4: Critic Review ----
        st.subheader("🛡️ Critic Review")
        review = critic.review(user_query, execution_result, answer)

        if review["approved"]:
            st.success(f"Approved ✅ — {review['reason']}")
        else:
            st.error(f"Rejected ❌ — {review['reason']}")
