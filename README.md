# agents
Agents making my life easier.

Core Architecture Components
1. Foundation Model: Llama 3 as the base LLM
    * Will power all agent reasoning capabilities
    * Can be run locally or via API depending on your compute resources
2. LlamaIndex Framework
    * Provides agent structuring, RAG capabilities, and tool integration
    * Handles context management and query routing
3. Specialized Agents
    * Planning Agent: Coordinates workflows and breaks down tasks
    * Calendar Agent: Manages scheduling and time-based activities
    * Email Agent: Handles email drafting, summarization, and organization
    * Research Agent: Gathers information from various sources
    * Memory Agent: Retrieves past interactions and maintains context
    * Task Agent: Executes specific actions and reports results
4. Shared Memory & Orchestration
    * Maintains state between agent interactions
    * Routes messages between specialized agents
    * Tracks task completion status
5. Chroma Vector Database
    * Stores embeddings for documents, past interactions, and knowledge
    * Enables semantic search for relevant context
6. External API Connections
    * Calendar services
    * Email providers
    * Web search capabilities
