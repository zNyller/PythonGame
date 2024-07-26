from typing import Any, Dict, Optional

class EventManager:
    """Gerencia eventos do jogo."""

    def __init__(self) -> None:
        """Inicializa o dicionário para armazenar os listeners por tipo de evento."""
        self.listeners = {}

    def subscribe(self, event_type: str, listener: object) -> None:
        """Inscreve um listener em um tipo específico de evento."""
        if event_type not in self.listeners:
            self.listeners[event_type] = [] 
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener: object) -> None:
        """Remove um listener registrado para um tipo específico de evento, caso exista."""
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)

    def notify(self, event: Dict[str, Any]) -> Optional[Any]:
        """Notifica os listeners inscritos no tipo de evento.
        
        Verifica se o tipo do evento recebido existe no dicionário de listeners,
        caso exista, chama o método notify do listener e armazena o resultado (se houver).

        Args:
        - event: Um dicionário contendo pelo menos a chave 'type' que define o tipo de evento.

        Returns:
        - O resultado do primeiro listener que retornar um valor válido.
        - Retorna None se nenhum listener retornar um valor válido.
        """
        event_type = event.get('type')
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                result = listener.notify(event)
                if result is not None:
                    return result
        return None