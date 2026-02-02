import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3" 


class GeneratorAgent:
    """
    Generator Agent:
    - Uses a self-hosted LLM (Ollama)
    - Converts retrieved context into a final answer
    """
    
    def generate(self, user_query: str, execution_results: dict) -> str:
        
        context_blocks = []
        
        for item in execution_results.get("execution_results", []):
            action = item["action"]
            data = item["data"]

        if action == "search_milvus":
            contexts = data.get("contexts", [])
            context_blocks.extend(contexts)

        elif action == "read_excel":
            rows = data.get("rows", {})
            context_blocks.append(
                f"Excel data:\n{rows}"
            )
            
        context_blocks = context_blocks[:3]
            
        context_text = (
            "\n\n".join(context_blocks)
              if context_blocks
              else "No relevant context was retrieved."
        )

    

        prompt = f"""
        You are an enterprise AI assistant.
        Answer the user's question using ONLY facts that are explicitly present in the provided context.
        Keep the answer concise (max 5 sentences).
        
        Do NOT:
        - Assume the type of document
        - Infer intent, title, or category
        - Add interpretations or generalizations
        
        If the context does not clearly contain the requested information:
        - State that explicitly
        - Do not speculate

        Rules
        - Do not speculate beyond the context
        - Paraphrasing is allowed for descriptive questions
        - If you present a numbered or bulleted list:
        - Complete every item fully
        - Do not stop mid-sentence
        - Ensure all points are complete
        
        USER QUESTION:
        {user_query}
        CONTEXT:
        {context_text}
        
        ANSWER:
        
        """

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 512,
                    "temperature": 0.2
                }
            },

            timeout=120
        )
        response.raise_for_status()

        return response.json()["response"].strip()
