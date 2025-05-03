from src.agents.planning import PlanningAgent
from src.agents.calendar import CalendarAgent
from src.agents.email import EmailAgent
from src.agents.research import ResearchAgent
from src.agents.memory import MemoryAgent
from src.agents.task import TaskAgent
from src.framework.llamaindex import LlamaIndexFramework
from src.framework.orchestration import Orchestrator
from src.framework.shared_memory import SharedMemory
from src.foundation.llama3 import Llama3Model
from src.db.chroma import ChromaDB
from src.api.calendar import CalendarAPI
from src.api.email import EmailAPI
from src.api.web_search import WebSearchAPI

def main():
    # Initialize core components
    memory = SharedMemory()
    db = ChromaDB()
    model = Llama3Model()
    framework = LlamaIndexFramework(model, db)

    # Initialize APIs
    calendar_api = CalendarAPI()
    email_api = EmailAPI()
    web_search_api = WebSearchAPI()

    # Initialize agents
    agents = {
        "planning": PlanningAgent("PlanningAgent", memory, [framework]),
        "calendar": CalendarAgent("CalendarAgent", memory, [calendar_api]),
        "email": EmailAgent("EmailAgent", memory, [email_api]),
        "research": ResearchAgent("ResearchAgent", memory, [web_search_api]),
        "memory": MemoryAgent("MemoryAgent", memory, [db]),
        "task": TaskAgent("TaskAgent", memory, []),
    }

    orchestrator = Orchestrator(agents, memory)

    # Example: route a task
    task = {"type": "schedule_meeting", "details": "..."}
    context = {}
    orchestrator.route(task, context)

if __name__ == "__main__":
    main()
