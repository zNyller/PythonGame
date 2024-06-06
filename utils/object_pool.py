class ObjectPool:
    def __init__(self, factory):
        self.factory = factory
        self.pool = []

    
    def get(self, *args, **kwargs):
        if self.pool:
            obj = self.pool.pop()
            if hasattr(obj, 'reset'):
                obj.reset() # Resetar objeto para o estado inicial
            return obj
        else:
            return self.factory(*args, **kwargs)


    def release(self, obj):
        self.pool.append(obj)