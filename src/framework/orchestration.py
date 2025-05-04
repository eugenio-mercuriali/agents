import logging
from typing import Optional

from src.agents.base import BaseAgent
from src.foundation.llm import LLM
from src.register.registries import available_agents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Task assistant system."""

    def __init__(self, llm: LLM, agents: Optional[dict[str, BaseAgent]] = None):
        self.llm = llm
        self.agents = self._init_agents if not agents else agents

    def _init_agents(self) -> None:
        """Initialize all specialized agents."""
        for agent in available_agents.classes():
            initialized_agent = agent(self.llm.model)
            self.agents[initialized_agent.agent_name] = initialized_agent.agent

    def process_user_request(self, user_request: str) -> str:
        """
        Process a user request through the multi-agent system.

        Args:
            user_request: User's request text

        Returns:
            Response to the user
        """
        logger.info(f"Processing user request: {user_request}")

        # Store the request in memory
        if "memory" in self.agents:
            self.agents["memory"].store_memory(user_request, tags=["user_request"])

        # Always start with the planning agent
        planning_response = self.agents["planning"].chat(user_request)

        # The planning agent will delegate to other agents as needed through tools
        return planning_response.response
