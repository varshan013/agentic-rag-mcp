class CriticAgent:
    """
    Generalized Critic Agent:
    - Document-agnostic
    - Allows semantic summaries for descriptive queries
    - Enforces strict grounding for factual queries
    """

    def review(self, user_query: str, execution_results: dict, generated_answer: str) -> dict:
        query_lower = user_query.lower()
        answer_lower = generated_answer.lower()

        #  1. Detect descriptive intent
        descriptive_starters = [
            "what is",
            "what are",
            "summarize",
            "summary",
            "overview",
            "describe",
            "explain",
            "tell me about",
            "give an overview",
            "what does it"
        ]

        is_descriptive = any(query_lower.startswith(k) for k in descriptive_starters)

        #  2. Collect retrieved context
        retrieved_text = []

        for item in execution_results.get("execution_results", []):
            data = item.get("data", {})
            if "contexts" in data:
                retrieved_text.extend(data["contexts"])
            if "rows" in data:
                retrieved_text.append(str(data["rows"]))

        combined_context = " ".join(retrieved_text).lower()

        if not combined_context.strip():
            return {
                "approved": False,
                "reason": "No retrieved context available"
            }

        #  3. Descriptive queries
        if is_descriptive:
            return {
                "approved": True,
                "reason": "Descriptive query – semantic summary allowed"
            }

        #  4. Factual queries 
        factual_overlap = any(
            sentence.strip() in combined_context
            for sentence in answer_lower.split(".")
            if len(sentence.strip()) > 10
        )

        if factual_overlap:
            return {
                "approved": True,
                "reason": "Factual answer grounded in retrieved context"
            }

        return {
            "approved": False,
            "reason": "Factual answer not grounded in retrieved context"
        }
