import json
from datetime import datetime
from typing import Any, ClassVar

from llama_index.core import Document
from llama_index.core.tools import FunctionTool, QueryEngineTool

from src.agents.base import BaseAgent


class MemoryAgent(BaseAgent):
    """
    Retrieves past interactions and maintains context.
    """

    agent_name: ClassVar[str] = "memory"

    @property
    def system_prompt(self) -> str:
        """Memory agent prompt."""

        system_prompt = """You are the Memory Agent in a multi-agent system.
        Your job is to:
        1. Store important information for long-term recall
        2. Retrieve relevant context when needed
        3. Update memories with new information
        4. Help maintain conversation continuity

        Always prioritize recent and relevant information for the current task.
        """

        return system_prompt

    def tools(self) -> list[FunctionTool]:
        """Create the memory management agent."""
        # Tools for the memory agent
        tools = [
            FunctionTool.from_defaults(
                fn=self._store_memory,
                name="store_memory",
                description="Store information in long-term memory",
            ),
            FunctionTool.from_defaults(
                fn=self._retrieve_memory,
                name="retrieve_memory",
                description="Retrieve information from memory based on query",
            ),
            FunctionTool.from_defaults(
                fn=self._update_memory,
                name="update_memory",
                description="Update existing memory with new information",
            ),
        ]

        # Vector index for memory storage
        memory_index = self.vector_database.setup_vector_index("memory_store")
        query_engine = memory_index.as_query_engine()

        tools.append(
            QueryEngineTool.from_defaults(
                query_engine=query_engine,
                name="memory_query",
                description="Query semantic memory database for relevant information",
            )
        )

        return tools

    def _store_memory(self, content: str, tags: list[str] = None) -> str:
        """
        Store information in long-term memory.

        Args:
            content: Content to store
            tags: Tags for categorization

        Returns:
            Memory ID
        """
        if tags is None:
            tags = []

        memory_id = f"memory_{hash(content)}"

        # TODO: index doc properly
        # Create a document for vector storage
        doc = Document(
            text=content,
            metadata={"tags": tags, "created_at": datetime.now().isoformat()},
        )

        # Get the memory collection
        collection = self.chroma_client.get_or_create_collection("memory_store")

        # Generate embeddings and store
        embedding = self.embed_model.get_text_embedding(content)
        collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            metadatas=[
                {"tags": json.dumps(tags), "created_at": datetime.now().isoformat()}
            ],
            documents=[content],
        )

        return memory_id

    def _retrieve_memory(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """
        Retrieve information from memory based on query.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of memories
        """
        # Get the memory collection
        collection = self.chroma_client.get_or_create_collection("memory_store")

        # Generate query embedding
        embedding = self.embed_model.get_text_embedding(query)

        # Search
        results = collection.query(query_embeddings=[embedding], n_results=top_k)

        # Format results
        memories = []
        for i in range(len(results["ids"][0])):
            memories.append(
                {
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": (
                        json.loads(results["metadatas"][0][i]["tags"])
                        if "tags" in results["metadatas"][0][i]
                        else {}
                    ),
                }
            )

        return memories

    def _update_memory(self, memory_id: str, new_content: str) -> str:
        """
        Update existing memory with new information.

        Args:
            memory_id: ID of memory to update
            new_content: New content

        Returns:
            Status message
        """
        # Get the memory collection
        collection = self.chroma_client.get_or_create_collection("memory_store")

        # Generate embedding for new content
        embedding = self.embed_model.get_text_embedding(new_content)

        # Update the document
        try:
            collection.update(
                ids=[memory_id], embeddings=[embedding], documents=[new_content]
            )
            return f"Memory {memory_id} updated successfully"
        except Exception as e:
            return f"Error updating memory: {e!s}"
