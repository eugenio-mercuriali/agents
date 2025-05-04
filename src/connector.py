"""Shared memory object."""

class Connector:
    """Allow agents to access the same components"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Connector, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.shared_memory = {}


