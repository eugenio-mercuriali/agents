"""LLM module."""

import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLM:
    """Language model class. Uses either a remote or local model."""

    def __init__(self, api_key: str = None):

        self.api_key = api_key
        self._model = None

    @property
    def model(self) -> Any:
        """LLM model object."""
        if self._model is None:
            self._model = self._init_llm()
        return self._model

    def _init_llm(self) -> Any:
        """Initialize the LLM using an inference API or a local Ollama model.
        Returns:
            LLM interface object
        """
        # Use OpenAI-compatible API with LlamaIndex if an api key is provided
        if self.api_key and self.api_key.startswith("sk-"):
            from llama_index.llms.openai import OpenAI

            return OpenAI(
                api_key=self.api_key,
                model="gpt-3.5-turbo",
                temperature=0.1,
                max_tokens=1024
            )

        # If an api key is not provided, use Ollama API (free, self-hosted or via cloud service)
        else:
            try:
                from llama_index.llms.ollama import Ollama
                return Ollama(
                    model="llama3:8b",
                    temperature=0.1,
                    request_timeout=120.0,
                    base_url="http://localhost:11434"  # Change if using remote Ollama instance
                )
            except Exception as e:
                logger.error(f"Error initializing Ollama: {e}")

    def generate(self, prompt, context=None):
        # Call the model to generate a response
        pass
