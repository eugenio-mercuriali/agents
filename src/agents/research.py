from typing import ClassVar

from src.agents.base import BaseAgent


class ResearchAgent(BaseAgent):
    """
    Gathers information from various sources.
    """

    agent_name: ClassVar[str] = "research"

    @property
    def system_prompt(self) -> str:
        system_prompt = """You are the Research Agent in a multi-agent system.
        Your job is to:
        1. Find relevant information on topics
        2. Synthesize data from multiple sources
        3. Present findings in a clear, structured way
        4. Identify key insights and patterns

        Always cite sources and verify information when possible.
        """
        return system_prompt
