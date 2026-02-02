import requests

MCP_BASE_URL = "http://localhost:8001"


class PlannerAgent:
    """
    Planner Agent:
    - Discovers MCP tools
    - Produces single-step or multi-step execution plans
    """

    def __init__(self):
        self.tools = self._discover_tools()

    def _discover_tools(self):
        resp = requests.get(f"{MCP_BASE_URL}/list_tools")
        resp.raise_for_status()
        return resp.json()

    def plan(self, user_query: str) -> dict:
        query = user_query.lower()
        steps = []

        # Greeting
        if query in ["hi", "hello", "hey"]:
            return {
                "steps": [
                    {"action": "chat", "reason": "Greeting detected"}
                ]
            }

        # Excel only
        if "excel" in query or "csv" in query:
            steps.append({
                "action": "read_excel",
                "reason": "Tabular data required"
            })

        # Document retrieval
        if any(word in query for word in ["pdf", "document", "policy", "report", "summary"]):
            steps.append({
                "action": "search_milvus",
                "reason": "Document context required"
            })

        # Comparison / complex query → multi-step
        if "compare" in query and len(steps) > 1:
            return {"steps": steps}

        # Default fallback
        if not steps:
            steps.append({
                "action": "search_milvus",
                "reason": "Default retrieval"
            })

        return {"steps": steps}
