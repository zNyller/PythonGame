class EventManager:
    """Gerencia eventos do jogo."""
    def __init__(self):
        self.listeners = {} # Dicionário para armazenar os listeners por tipo de evento


    def subscribe(self, event_type, listener):
        """
        Registra um listener para um tipo específico de evento.

        Args:
        - event_type (str): Tipo de evento ao qual o listener irá responder.
        - listener (object): Objeto que possui um método `notify(event)` para lidar com o evento.
        """

        if event_type not in self.listeners:
            self.listeners[event_type] = [] # Cria uma nova lista vazia se o tipo de evento ainda não foi registrado
        self.listeners[event_type].append(listener) # Adiciona o listener à nova lista de listeners do evento específico


    def unsubscribe(self, event_type, listener):
        """
        Remove um listener registrado para um tipo específico de evento, se existir.

        Args:
        - event_type (str): Tipo de evento do qual o listener deve ser removido.
        - listener (object): Listener a ser removido.
        """

        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener) # Remove o listener se ele estiver presente na lista


    def notify(self, event):
        """
        Notifica todos os listeners registrados para um tipo específico de evento.

        Args:
        - event (dict): Dicionário contendo informações sobre o evento, incluindo o tipo do evento ('type').

        Returns:
        - O resultado do primeiro listener que retornar um valor válido.
        - Retorna None se nenhum listener retornar um valor válido.
        """

        event_type = event.get('type') # Obtém o tipo de evento do dicionário de evento
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                result = listener.notify(event) # Chama o método `notify(event)` do listener e armazena o resultado
                if result is not None:
                    return result
        return None