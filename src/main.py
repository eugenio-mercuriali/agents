from agents.planning import PlanningAgent
from agents.calendar import CalendarAgent
from agents.email import EmailAgent
from agents.research import ResearchAgent
from agents.memory import MemoryAgent
from agents.task import TaskAgent
from framework.llamaindex import LlamaIndexFramework
from framework.orchestration import Orchestrator
from framework.shared_memory import SharedMemory
from foundation.llama3 import Llama3Model
from db.chroma import ChromaDB
from api.calendar import CalendarAPI
from api.email import EmailAPI
from api.web_search import WebSearchAPI

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
