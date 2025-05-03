from .base import BaseAgent
from typing import Any, Dict

class EmailAgent(BaseAgent):
    """
    Handles email drafting, summarization, and organization.
    """
    def handle(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        email_api = self.tools[0]
        if task.get("type") == "send_email":
            to, subject, body = task["to"], task["subject"], task["body"]
            result = email_api.send_email(to, subject, body)
            return {"status": "sent", "result": result}
        elif task.get("type") == "summarize_email":
            email_content = task["content"]
            summary = self._summarize(email_content)
            return {"status": "summarized", "summary": summary}
        return {"status": "ignored", "reason": "Unknown task type"}

    def _summarize(self, content: str) -> str:
        # Placeholder: Use LLM or simple summarization
        return content[:100] + "..." if len(content) > 100 else content