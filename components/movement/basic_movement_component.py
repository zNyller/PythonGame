import pygame
from .movement_interface import MovementComponent
from managers.event_manager import EventManager
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY

class BasicMovementComponent(MovementComponent):
    """Componente de movimento para as entidades do jogo.

    Gerencia o movimento com base nas teclas pressionadas e limita entre as bordas da janela.
    """
    def __init__(
            self, 
            entity_rect: pygame.Rect, 
            movement_speed: int, 
            event_manager: EventManager
        ) -> None:
        super().__init__()
        self.entity_rect = entity_rect
        self.movement_speed = movement_speed
        self.event_manager = event_manager
        self.state = 'idle'
        self.facing_right = True
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Inscreve os eventos necessários no Event Manager."""
        self.event_manager.subscribe('player_attack', self)

    def update(self, player_rect: pygame.Rect, delta_time: float) -> None:
        """Atualiza os movimentos."""
        if self.state == 'idle':
            self.handle_movements(delta_time)
        if player_rect:
            self.sync_player_rect(player_rect)
        self.limits_movements(LEFT_BOUNDARY, RIGHT_BOUNDARY)

    def handle_movements(self, delta_time: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_left(delta_time)
            self.facing_right = False
        if keys[pygame.K_d]:
            self.move_right(delta_time)
            self.facing_right = True

    def move_left(self, delta_time: float) -> None:
        """Move a entidade para a esquerda."""
        self.entity_rect.x -= self.movement_speed * delta_time

    def move_right(self, delta_time: float) -> None:
        """Move a entidade para a direita."""
        self.entity_rect.x += self.movement_speed * delta_time

    def sync_player_rect(self, player_rect: pygame.Rect) -> None:
        """Sincroniza o centro do player_rect com o centro de entity_rect do componente."""
        player_rect.centerx = self.entity_rect.centerx

    def limits_movements(self, left_boundary: int, right_boundary: int) -> None:
        """Limita os movimentos da entidade dentro da janela de jogo."""
        self.entity_rect.left = max(self.entity_rect.left, left_boundary)
        self.entity_rect.right = min(self.entity_rect.right, right_boundary)

    def notify(self, event: dict) -> None:
        if event['type'] == 'player_attack':
            self.state = 'attacking' if event['state'] == 'start' else 'idle'