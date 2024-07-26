import pygame
from typing import Tuple
from config.constants import BLUE_LIFEBAR
from core.camera import Camera
from managers.event_manager import EventManager
from entities.mob import Mob

class LifeBarComponent:
    """Gerencia a posição e dimensões da barra de vida com base no status da entidade.

    Desenha a barra de vida na tela.
    """
    def __init__(
            self, 
            entity: Mob, 
            event_manager: EventManager, 
            width: int, 
            height: int, 
            color: Tuple[int, int, int]
        ) -> None:
        """Inicializa os atributos para configurar a barra de vida."""
        self.entity = entity
        self.event_manager = event_manager
        self.width = width
        self.height = height
        self.color = color
        self.max_life = entity.life
        self.current_life = self.previous_life = entity.life
        self.entity_rect = entity.rect
        self.outline = self.create_life_bar(
            self.entity_rect.centerx, 
            self.entity_rect.top, 
            self.width, 
            self.height
        )
        self.inner = self.create_life_bar(
            self.entity_rect.centerx, 
            self.entity_rect.top, 
            self.width, 
            self.height
        )
        self.event_manager.subscribe('damage_event', self)

    def notify(self, event):
        """Chama os métodos inscritos no tipo do evento recebido."""
        if event['type'] == 'damage_event' and event['target'] == self.entity:
            self.update_life_bar()

    def create_life_bar(self, centerx, top, width, height):
        """Cria e retorna a barra de vida utilizando as medidas apropriadas."""
        return pygame.Rect(centerx - width // 2, top -15, width, height)

    def draw_life_bar(self, screen: pygame.Surface, camera: Camera):
        """ Desenha a barra de vida e seu contorno na tela considerando a câmera. """
        self._update_life_bar_position()
        outline_pos = camera.apply(self.outline)
        inner_pos = camera.apply(self.inner)
        pygame.draw.rect(screen, self.color, inner_pos, border_radius=5)
        pygame.draw.rect(screen, BLUE_LIFEBAR, outline_pos, width=2, border_radius=5)

    def update_life_bar(self) -> None:
        """Atualiza a barra de vida da entidade quando houver alteração."""
        self.current_life = self.entity.life
        if self.current_life > 0:
            # Calcula a largura proporcional da barra interna
            self.inner.width = int(self.width * (self.current_life / self.max_life))
            self.previous_life = self.current_life
        else:
            self.inner.width = 0
        self._update_life_bar_position()

    def _update_life_bar_position(self) -> None:
        """Atualiza a posição da barra de acordo com a posição da entidade."""
        self.outline.centerx = self.entity_rect.centerx 
        self.inner.centerx = self.entity_rect.centerx
        self.outline.top = self.entity_rect.top -15
        self.inner.top = self.entity_rect.top -15