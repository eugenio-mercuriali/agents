from .base import BaseAgent
from typing import Any, Dict

class MemoryAgent(BaseAgent):
    """
    Retrieves past interactions and maintains context.
    """
    def handle(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        db = self.tools[0]
        if task.get("type") == "retrieve_memory":
            query = task["query"]
            results = db.search(query)
            return {"status": "retrieved", "results": results}
        elif task.get("type") == "store_memory":
            doc_id, embedding, metadata = task["doc_id"], task["embedding"], task.get("metadata")
            db.add_embedding(doc_id, embedding, metadata)
            return {"status": "stored"}
        return {"status": "ignored", "reason": "Unknown task type"}