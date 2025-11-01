class Memory:
    def __init__(self):
        self._memory = 0
    
    def memory_add(self, value):
        """M+ - добавить значение к памяти"""
        self._memory += float(value)
    
    def memory_subtract(self, value):
        """M- - вычесть значение из памяти"""
        self._memory -= float(value)
    
    def memory_recall(self):
        """MR - получить значение из памяти"""
        return self._memory
    
    def memory_clear(self):
        """MC - очистить память"""
        self._memory = 0
    
    def memory_store(self, value):
        """MS - сохранить значение в память"""
        self._memory = float(value)
    
    def get_memory_value(self):
        return self._memory