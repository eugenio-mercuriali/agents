class BaseAgent:
    def __init__(self, name, memory, tools):
        self.name = name
        self.memory = memory
        self.tools = tools

    def handle(self, task, context):
        raise NotImplementedError("Each agent must implement the handle method.")
