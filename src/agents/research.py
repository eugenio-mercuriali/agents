from .base import BaseAgent
from typing import Any, Dict

class ResearchAgent(BaseAgent):
    """
    Gathers information from various sources.
    """
    def handle(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        web_search_api = self.tools[0]
        if task.get("type") == "web_search":
            query = task["query"]
            results = web_search_api.search(query)
            self.memory.set(f"search_{query}", results)
            return {"status": "completed", "results": results}
        return {"status": "ignored", "reason": "Unknown task type"}