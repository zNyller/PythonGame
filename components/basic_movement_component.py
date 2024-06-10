import pygame
from components.movement_component import MovementComponent
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY

class BasicMovementComponent(MovementComponent):
    """
    Componente de movimento para as entidades do jogo.

    Este componente gerencia o movimento com base nas teclas pressionadas e limita entre as bordas da janela
    """
    def __init__(self, entity_rect, movement_speed, event_manager):
        super().__init__()
        self.entity_rect = entity_rect
        self.movement_speed = movement_speed
        self.event_manager = event_manager
        self.state = 'idle'

        self.event_manager.subscribe('player_attack', self)


    def update(self, player_rect):
        self.handle_movements()
        self.sync_player_rect(player_rect)
        self.limits_movements(LEFT_BOUNDARY, RIGHT_BOUNDARY)


    def handle_movements(self):
        """Gerencia os movimentos com base na tecla pressionada"""

        if self.state == 'idle':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                # Move para a esquerda
                self.entity_rect.x -= self.movement_speed
            if keys[pygame.K_d]:
                # Move para a direita
                self.entity_rect.x += self.movement_speed
        elif self.state == 'attacking':
            ...


    def sync_player_rect(self, player_rect):
        """Sincroniza o centro do player_rect com o centro de entity_rect do componente"""
        player_rect.centerx = self.entity_rect.centerx


    def limits_movements(self, left_boundary, right_boundary):
        """Limita os movimentos da entidade dentro da janela de jogo."""

        self.entity_rect.left = max(self.entity_rect.left, left_boundary)
        self.entity_rect.right = min(self.entity_rect.right, right_boundary)


    def notify(self, event):
        if event['type'] == 'player_attack' and event['state'] == 'start':
            self.state = 'attacking'
        elif event['type'] == 'player_attack' and event['state'] == 'end':
            self.state = 'idle'