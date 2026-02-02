import requests

MCP_BASE_URL = "http://localhost:8001"


class ExecutionAgent:
    """
    Execution Agent:
    - Executes planner steps
    - Calls MCP tools
    """

    def execute(self, plan: dict, user_query: str) -> dict:
        results = []

        for step in plan.get("steps", []):
            action = step["action"]

            if action == "search_milvus":
                resp = requests.post(
                    f"{MCP_BASE_URL}/tool/search_milvus",
                    json={"query": user_query, "top_k": 5}
                )
                resp.raise_for_status()
                results.append({
                    "action": action,
                    "data": resp.json()
                })

            elif action == "read_excel":
                resp = requests.post(
                    f"{MCP_BASE_URL}/tool/read_excel",
                    json={"file_path": "data/sample.xlsx"}
                )
                resp.raise_for_status()
                results.append({
                    "action": action,
                    "data": resp.json()
                })

            elif action == "chat":
                results.append({
                    "action": "chat",
                    "data": {"message": "Hello! How can I help you?"}
                })

        return {
            "execution_results": results
        }
