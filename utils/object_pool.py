class ObjectPool:
    """ Um pool de objetos reutilizáveis gerenciado por uma função de fábrica para criar novos objetos. """

    def __init__(self, factory):
        """ Inicializa o ObjectPool com uma função de fábrica para criar objetos. """
        self.factory = factory
        self.pool = []


    def get(self, *args, **kwargs) -> object:
        """ Obtém um objeto do pool, se disponível, ou cria um novo usando a função de fábrica. """
        if self.pool:
            obj = self.pool.pop()
            if hasattr(obj, 'reset'):
                obj.reset()  # Reinicia o objeto para o estado inicial, se tiver o método reset
            return obj
        else:
            return self.factory(*args, **kwargs)


    def release(self, *objects):
        """ Libera um ou mais objetos de volta ao pool para reutilização."""
        for obj in objects:
            self.pool.append(obj)