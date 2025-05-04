from typing import Any, Dict, ClassVar
from datetime import datetime

from src.agents.base import BaseAgent
from llama_index.core.tools import FunctionTool, QueryEngineTool, BaseTool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlanningAgent(BaseAgent):
    """
    Coordinates workflows and breaks down tasks into subtasks.
    """

    agent_name: ClassVar[str] = "planning"

    def __init__(self, llm: Any, agents: dict[str]):
        super().__init__(llm)
        self.agents = agents

    @property
    def system_prompt(self) -> str:
        """Planning agent prompt."""
        system_prompt = """You are the Planning Agent in a multi-agent system.
        Your job is to:
        1. Break down user requests into subtasks
        2. Delegate those subtasks to specialized agents
        3. Track progress and ensure task completion
        4. Report results back to the user
        
        Always think step by step and coordinate with other agents effectively.
        """
        return system_prompt

    @property
    def tools(self) -> list[BaseTool] | None:
        tools = [
            FunctionTool.from_defaults(
                fn=self._delegate_task,
                name="delegate_task",
                description="Delegate a specific task to another agent"
            ),
            FunctionTool.from_defaults(
                fn=self._create_task_sequence,
                name="create_task_sequence",
                description="Create a sequence of tasks to accomplish a goal"
            ),
        ]

        # Vector index for planning knowledge
        planning_index = self.vector_database.setup_vector_index("planning_knowledge")
        query_engine = planning_index.as_query_engine()

        tools.append(
            QueryEngineTool.from_defaults(
                query_engine=query_engine,
                name="planning_knowledge",
                description="Query planning knowledge base for task planning strategies"
            )
        )

        return tools

    def _delegate_task(self, agent_name: str, task_description: str, priority: str = "normal") -> str:
        """
        Delegate a task to a specific agent.

        Args:
            agent_name: Name of the agent to delegate to
            task_description: Description of the task
            priority: Priority level (high, normal, low)

        Returns:
            Status message
        """
        if agent_name not in self.agents:
            return f"Error: Agent '{agent_name}' not found"

        # Add task to shared memory
        task_id = f"task_{len(self.connector.shared_memory.get('tasks', []))}"

        if "tasks" not in self.shared_memory:
            self.shared_memory["tasks"] = []

        task = {
            "id": task_id,
            "description": task_description,
            "assigned_to": agent_name,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "result": None
        }

        self.shared_memory["tasks"].append(task)

        logger.info(f"Task {task_id} delegated to {agent_name}: {task_description}")
        return f"Task {task_id} successfully delegated to {agent_name}"

    def _create_task_sequence(self, goal: str, sub_tasks: list[Dict[str, Any]]) -> str:
        """
        Create a sequence of tasks to accomplish a goal.

        Args:
            goal: Overall goal to accomplish
            sub_tasks: List of subtasks with agent assignments

        Returns:
            Task sequence ID
        """
        sequence_id = f"sequence_{len(self.shared_memory.get('sequences', []))}"

        if "sequences" not in self.shared_memory:
            self.shared_memory["sequences"] = []

        sequence = {
            "id": sequence_id,
            "goal": goal,
            "sub_tasks": sub_tasks,
            "status": "in_progress",
            "created_at": datetime.now().isoformat(),
            "completed_tasks": []
        }

        self.shared_memory["sequences"].append(sequence)

        # Create individual tasks for each subtask
        for idx, subtask in enumerate(sub_tasks):
            self._delegate_task(
                agent_name=subtask["agent"],
                task_description=subtask["description"],
                priority=subtask.get("priority", "normal")
            )

        logger.info(f"Task sequence {sequence_id} created for goal: {goal}")
        return f"Task sequence {sequence_id} created with {len(sub_tasks)} subtasks"