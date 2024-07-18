import pygame
from entities.player import Player
from entities.mob import Mob

class Camera:
    """Câmera que acompanha as entidades."""

    MARGIN = 50

    def __init__(self, width, height, map_width, map_height) -> None:
        """Inicializa a câmera definindo suas coordenadas."""
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity: Player | Mob) -> pygame.Rect:
        """Aplica a câmera à entidade."""
        if hasattr(entity, 'rect'):
            return entity.rect.move(self.camera.topleft)
        return entity.move(self.camera.topleft)

    def update(self, target: Player | Mob) -> None:
        """Atualiza a posição da câmera com base na posição do alvo."""
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limita a câmera aos limites do mapa
        x = max(min(x, 0), -(self.map_width - self.width))  # Lados esquerdo e direito
        y = max(min(y, 0), -(self.map_height - self.height))  # Parte superior e inferior
        self.camera = pygame.Rect(x, y, self.width, self.height)