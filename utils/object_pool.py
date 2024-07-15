class ObjectPool:
    """ Um pool de objetos reutilizáveis gerenciado por uma função de fábrica para criar novos objetos. """

    def __init__(self, factory):
        """ Inicializa o ObjectPool com uma função de fábrica para criar objetos. """
        self.factory = factory
        self.pool = []


    def get(self, *args, **kwargs) -> object:
        """ Obtém um objeto resetado (caso contenha atributo 'reset') do pool, se disponível, 
        ou cria um novo objeto usando a função de fábrica com base no 'name'. 
        """
        name = kwargs.get('name')
        for obj in self.pool:
            if obj.type == name:
                self.pool.remove(obj)
                if hasattr(obj, 'reset'):
                    obj.reset() # Caso contenha o método reset, reseta para o estado inicial.
                return obj
        return self.factory(*args, **kwargs)


    def release(self, *objects):
        """ Libera um ou mais objetos de volta ao pool para reutilização. """
        for obj in objects:
            self.pool.append(obj)