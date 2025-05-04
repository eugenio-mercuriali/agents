from abc import ABC, abstractmethod

from class_registry.base import AutoRegister
from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import FunctionTool

from src.connector import Connector
from src.constants import TOKEN_LIMIT
from src.db.chroma import ChromaDB
from src.foundation.llm import LLM
from src.register.registries import available_agents


class BaseAgent(AutoRegister(available_agents), ABC):
    """
    Abstract base class for all agents.
    """

    connector: Connector = Connector()

    def __init__(self, llm: LLM, vector_database: ChromaDB = None):
        self.llm = llm
        self.vector_database = vector_database
        self._memory = None

    @property
    @abstractmethod
    def tools(self) -> list[FunctionTool]:
        """Tools for the agent."""
        pass

    @abstractmethod
    def system_prompt(self) -> str:
        """Agent prompt."""
        pass

    @property
    def memory(self) -> ChatMemoryBuffer:
        """Memory for the agent."""
        if self._memory is None:
            self._memory = ChatMemoryBuffer.from_defaults(token_limit=TOKEN_LIMIT)
        return self._memory

    @property
    def agent(self) -> ReActAgent:
        """ReActAgent object."""
        return ReActAgent.from_tools(
            self.tools,
            llm=self.llm,
            memory=self.memory,
            system_prompt=self.system_prompt,
            verbose=True,
        )
