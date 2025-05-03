from .base import BaseAgent
from typing import Any, Dict

class PlanningAgent(BaseAgent):
    """
    Coordinates workflows and breaks down tasks into subtasks.
    """
    def handle(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        # Example: break down a high-level task into subtasks
        if task.get("type") == "plan_workflow":
            workflow = self._decompose_task(task["details"])
            self.memory.set("current_workflow", workflow)
            return {"status": "planned", "workflow": workflow}
        return {"status": "ignored", "reason": "Unknown task type"}

    def _decompose_task(self, details: Any) -> list:
        # Placeholder: Use LLM or rules to break down the task
        # For now, just split by sentences
        if isinstance(details, str):
            return [step.strip() for step in details.split('.') if step.strip()]
        return []