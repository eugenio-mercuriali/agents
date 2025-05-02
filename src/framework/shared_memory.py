class SharedMemory:
    def __init__(self):
        self.state = {}

    def get(self, key):
        return self.state.get(key)

    def set(self, key, value):
        self.state[key] = value
