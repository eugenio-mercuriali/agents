from .base import BaseAgent
from typing import Any, Dict

class CalendarAgent(BaseAgent):
    """
    Manages scheduling and time-based activities.
    """
    def handle(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        if task.get("type") == "schedule_event":
            event = task["event"]
            calendar_api = self.tools[0]
            result = calendar_api.schedule_event(event)
            self.memory.set(f"event_{event['id']}", result)
            return {"status": "scheduled", "event": result}
        return {"status": "ignored", "reason": "Unknown task type"}