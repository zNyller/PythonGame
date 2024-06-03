import pygame
from components.movement_component import MovementComponent

class BasicMovementComponent(MovementComponent):
    """
    Componente de movimento para as entidades do jogo.

    Este componente gerencia o movimento com base nas teclas pressionadas e limita entre as bordas da janela
    """
    def __init__(self, entity_rect, movement_speed):
        super().__init__()
        self.entity_rect = entity_rect
        self.movement_speed = movement_speed


    def handle_movements(self):
        """Gerencia os movimentos com base na tecla pressionada"""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # Move para a esquerda
            self.entity_rect.x -= self.movement_speed
        if keys[pygame.K_d]:
            # Move para a direita
            self.entity_rect.x += self.movement_speed


    def limits_movements(self, left_boundary, right_boundary):
        """Limita os movimentos da entidade dentro da janela de jogo."""

        self.entity_rect.left = max(self.entity_rect.left, left_boundary)
        self.entity_rect.right = min(self.entity_rect.right, right_boundary)