import pygame
from typing import TYPE_CHECKING, Union
from ..animation.animation_interface import AnimationComponent

if TYPE_CHECKING:
    from entities.player import Player
    from entities.mob import Mob

class AttackAnimationComponent(AnimationComponent):
    """Gerencia as animações de ataque."""

    ATTACK_DURATION = 1.1
    ANIMATION_SPEED = 16
    CANNON_ATTACK_DURATION = 2.5
    CANNON_ANIMATION_SPEED = 29

    def __init__(self, entity: Union['Player', 'Mob']) -> None:
        super().__init__()
        self.entity = entity
        self._attack_type = None
        self.duration_timer = 0
        self._initial_rect = entity.rect.copy()

    def start_animation(self, attack_type: int) -> None:
        """Inicia a animação de acordo com o tipo de ataque."""
        self._attack_type = attack_type
        if attack_type == 1:
            self.animation_speed = self.ANIMATION_SPEED
            self.duration_timer = self.ATTACK_DURATION
        elif attack_type == 2:
            self.animation_speed = self.CANNON_ANIMATION_SPEED
            self.duration_timer = self.CANNON_ATTACK_DURATION

    def update(self, delta_time: float) -> None:
        """Avança os frames da animação de ataque."""
        if self.duration_timer > 0:
            self._update_frame(delta_time)
            self.duration_timer -= delta_time
        else:
            self.reset()

    def _update_frame(self, delta_time: float) -> None:
        """Atualiza o frame counter e a imagem do entity."""
        self.frame_counter += self.animation_speed * delta_time
        if self.frame_counter >= 1:
            self.frame_counter = -1
            self._increment_frame_index()
        self._update_entity_image()

    def _increment_frame_index(self) -> None:
        """Incrementa o índice de frame de acordo com o tipo de ataque e verifica se percorreu todos os frames."""
        frames = self.entity.attack_frames if self.attack_type == 1 else self.entity.cannon_frames
        self.current_frame_index += 1
        if self.current_frame_index >= len(frames):
            self.current_frame_index = 0

    def _update_entity_image(self) -> None:
        """Atualiza a imagem do entity com base no frame de ataque atual."""
        self.entity.image = self._get_current_frame()
        if self.entity.movement_component.facing_right:
            self.entity.image = pygame.transform.flip(self.entity.image, True, False)
        self.entity.rect = self.entity.image.get_rect(centerx=self.entity.rect.centerx, bottom=self._initial_rect.bottom + 6)

    def _get_current_frame(self) -> pygame.Surface:
        """Retorna o frame atual baseado no tipo de ataque."""
        return self.entity.attack_frames[self.current_frame_index] if self.attack_type == 1 else self.entity.cannon_frames[self.current_frame_index]
    
    @property
    def attack_type(self) -> int:
        return self._attack_type

    def reset(self) -> None:
        """Reseta os contadores e o tipo de ataque."""
        self.frame_counter = 0
        self.current_frame_index = 0
        self.duration_timer = 0
        self._attack_type = None