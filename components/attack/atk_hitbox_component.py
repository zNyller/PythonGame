import pygame
from typing import TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    from entities.player import Player
    from entities.mob import Mob

class AttackHitboxComponent:
    """Gerencia a hitbox de ataques de uma entidade."""

    def __init__(self, entity: Union['Player', 'Mob']) -> None:
        self._entity = entity
        self.attack_hitbox = pygame.Rect(0, 0, 50, 50)

    def update_hitbox(self, attack_type: int, current_frame_index: int) -> None:
        """Atualiza a hitbox de ataque com base no frame atual e na direção do jogador."""
        attack_width, attack_height = self._get_attack_hitbox_size(
            attack_type, 
            current_frame_index
        )
        # Atualiza a posição da hitbox com o offset calculado
        offset_x = 10 if self._entity.movement_component.facing_right else -10
        self.attack_hitbox.size = (attack_width, attack_height)
        self.attack_hitbox.centerx = self._entity.rect.centerx + offset_x
        self.attack_hitbox.bottom = self._entity.rect.bottom + 6

    def hit_target(self, target) -> bool:
        """Verifica se a hitbox atingiu o alvo."""
        return self.attack_hitbox.colliderect(target.rect)

    def _get_attack_hitbox_size(self, attack_type: int, current_frame_index: int) -> Tuple[int, int]:
        # Retorna o tamanho da hitbox de acordo com o tipo de ataque atual.
        return (
            self._get_sword_hitbox_size(current_frame_index) if attack_type == 1 
            else self._get_cannon_hitbox_size(current_frame_index)
        )

    def _get_sword_hitbox_size(self, current_frame_index: int) -> Tuple[int, int]:
        # Retorna o tamanho da hitbox baseado no frame atual.
        return (310, 250) if 3 < current_frame_index < 6 else (0, 0)

    def _get_cannon_hitbox_size(self, current_frame_index: int) -> Tuple[int, int]:
        # Retorna o tamanho da hitbox baseado no frame atual.
        if current_frame_index < 4:
            return (100, 150)
        elif current_frame_index < 16:
            return (250, 150)
        elif current_frame_index < 18:
            return (450, 150)
        elif current_frame_index < 20:
            return (520, 150)
        elif current_frame_index < 21:
            return (570, 150)
        elif current_frame_index < 22:
            return (590, 150)
        elif current_frame_index < 23:
            return (650, 150)
        elif current_frame_index < 24:
            return (670, 150)
        elif current_frame_index < 25:
            return (690, 150)
        else:
            return (100, 150)