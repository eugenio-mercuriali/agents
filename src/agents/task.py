from typing import ClassVar

from llama_index.core.tools import FunctionTool, QueryEngineTool

from src.agents.base import BaseAgent


class TaskAgent(BaseAgent):
    """
    Executes specific actions and reports results.
    """

    agent_name: ClassVar[str] = "task"

    def system_prompt(self) -> str:
        system_prompt = """You are the Task Agent in a multi-agent system.
        Your job is to:
        1. Execute assigned tasks efficiently
        2. Track task progress and status
        3. Report results and any issues encountered
        4. Learn from task execution patterns

        Always be thorough and detail-oriented in task execution.
        """
        return system_prompt

    def tools(self) -> list[FunctionTool]:
        tools = [
            FunctionTool.from_defaults(
                fn=self._execute_task,
                name="execute_task",
                description="Execute a specific defined task",
            ),
            FunctionTool.from_defaults(
                fn=self._check_task_status,
                name="check_task_status",
                description="Check the status of a task",
            ),
            FunctionTool.from_defaults(
                fn=self._report_task_result,
                name="report_task_result",
                description="Report the result of a completed task",
            ),
        ]

        # Vector index for task knowledge
        task_index = self.vector_database.setup_vector_index("task_knowledge")
        query_engine = task_index.as_query_engine()

        tools.append(
            QueryEngineTool.from_defaults(
                query_engine=query_engine,
                name="task_knowledge",
                description="Query knowledge base for task execution methodologies",
            )
        )

        return tools
