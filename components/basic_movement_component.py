import logging
# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        self.subscribe_to_events()


    def subscribe_to_events(self):
        """Inscreve os eventos necessários no Event Manager."""
        self.event_manager.subscribe('player_attack', self)


    def update(self, player_rect):
        """Atualiza os movimentos"""
        if self.state == 'idle':
            self.handle_movements()
        if player_rect:
            self.sync_player_rect(player_rect)
        self.limits_movements(LEFT_BOUNDARY, RIGHT_BOUNDARY)

    def handle_movements(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_d]:
            self.move_right()


    def move_left(self):
        if self.state != 'attacking':
            new_x = self.entity_rect.x - self.movement_speed
            self.entity_rect.x = new_x

    def move_right(self):
        if self.state != 'attacking':
            new_x = self.entity_rect.x + self.movement_speed
            self.entity_rect.x = new_x


    def sync_player_rect(self, player_rect):
        """Sincroniza o centro do player_rect com o centro de entity_rect do componente"""
        player_rect.centerx = self.entity_rect.centerx


    def limits_movements(self, left_boundary, right_boundary):
        """Limita os movimentos da entidade dentro da janela de jogo."""
        self.entity_rect.left = max(self.entity_rect.left, left_boundary)
        self.entity_rect.right = min(self.entity_rect.right, right_boundary)


    def notify(self, event):
        logging.debug(f'Received event: {event}')
        if event['type'] == 'player_attack':
            self.state = 'attacking' if event['state'] == 'start' else 'idle'
        logging.debug(f'Updated state to: {self.state}')