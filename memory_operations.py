class Memory:
    def __init__(self):
        self._memory = 0
    
    def memory_add(self, value):
        self._memory += float(value)
    
    def memory_subtract(self, value):
        self._memory -= float(value)
    
    def memory_recall(self):
        return self._memory
    
    def memory_clear(self):
        self._memory = 0
    
    def memory_store(self, value):
        self._memory = float(value)
    
    def get_memory_value(self):
        return self._memory