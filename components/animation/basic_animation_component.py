import pygame
from typing import List, Union, TYPE_CHECKING
from .animation_interface import AnimationComponent

if TYPE_CHECKING:
    from entities.player import Player
    from entities.mob import Mob
    from managers.event_manager import EventManager

class BasicAnimationComponent(AnimationComponent):
    """Gerencia a animação da entidade."""

    IDLE_ANIMATION_SPEED = 7

    def __init__(
            self: 'BasicAnimationComponent', 
            entity: Union['Player', 'Mob'], 
            animation_frames: List[pygame.Surface], 
            event_manager: 'EventManager'
        ) -> None:
        """Inicializa os atributos de animação."""
        super().__init__()
        self._entity = entity
        self._initial_animation_frames = self._animation_frames = animation_frames
        self._event_manager = event_manager
        self._initial_rect = entity.rect
        self._animation_speed = self.IDLE_ANIMATION_SPEED
        self._last_frame_index = -1  # Rastrear quando a imagem realmente muda
        self._state = self.IDLE_STATE
        self._event_manager.subscribe(event_type='damage_event', listener=self)

    def notify(self, event) -> None:
        if event['type'] == 'damage_event':
            self._animation_frames = event['animation_frames']

    def update(self, delta_time: float) -> None:
        """Incrementa o contador de animação e atualiza o frame."""
        self._increment_frame_counter(delta_time)
        self._update_current_frame()
        self._update_image()

    def _increment_frame_counter(self, delta_time: float) -> None:
        """Incrementa o frame counter baseado na velocidade da animação e delta time."""
        self.frame_counter += self._animation_speed * delta_time
        if self.frame_counter >= len(self._animation_frames):
            self.frame_counter = 0
            if self._animation_frames != self._initial_animation_frames:
                self._animation_frames = self._initial_animation_frames

    def _update_current_frame(self) -> None:
        """Atualiza o índice do frame atual baseado no frame counter."""
        self.current_frame_index = int(self.frame_counter)

    def _update_image(self) -> None:
        """Atualiza a imagem do sprite caso haja mudança de frames."""
        if self.current_frame_index != self._last_frame_index:
            self._entity.image = self._animation_frames[self.current_frame_index]
            if self._entity.movement_component.facing_right:
                self._entity.image = pygame.transform.flip(self._entity.image, True, False)
            self.rect = self._entity.image.get_rect(
                centerx=self._entity.rect.centerx, 
                bottom=self._initial_rect.bottom
            )