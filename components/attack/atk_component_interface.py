from abc import ABC, abstractmethod
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame.sprite import Sprite
    from entities.player import Player
    from entities.mob import Mob

class AttackComponent(ABC):
    """Classe abstrata para componentes de ataque.

    Define a interface que todos os componentes de ataque devem implementar.
    Possui métodos concretos para reutilização em subclasses.
    """

    ATTACK_STATE = 'attacking'
    IDLE_STATE = 'idle'
    KNOCKBACK_DISTANCE = 100

    def __init__(self, entity: Union['Player', 'Mob']) -> None:
        """Inicializa um componente de ataque."""
        self.entity = entity
        self.state = self.IDLE_STATE

    @abstractmethod
    def attack(self):
        """Método abstrato para iniciar a ação de ataque."""
        pass

    @abstractmethod
    def update(self, target_sprites: 'Sprite'):
        """Método abstrato para atualizar a ação de ataque."""
        pass

    @abstractmethod
    def _perform_attack(self, target_sprites: 'Sprite'):
        """Método abstrato para performar a ação de ataque."""
        pass

    @abstractmethod
    def _reset_attack(self):
        """Método abstrato para resetar a ação de ataque."""
        pass

    def inflict_damage(self, target: Union['Player', 'Mob'], damage: int) -> None:
        """Inflige dano ao alvo e verifica a vida restante."""
        target.receive_damage(damage)
        self._check_target_life(target)

    def knockback_target(self, target: Union['Player', 'Mob']) -> None:
        """Aplica efeito de recuo no alvo com base na sua posição."""
        target.rect.centerx += (
            self.KNOCKBACK_DISTANCE if target.rect.centerx > self.entity.rect.centerx 
            else -self.KNOCKBACK_DISTANCE
        )

    def knockback_entity(self, target: Union['Player', 'Mob']) -> None:
        """Aplica efeito de recuo na entidade com base na sua posição."""
        self.entity.rect.centerx += (
            self.KNOCKBACK_DISTANCE if self.entity.rect.centerx > target.rect.centerx 
            else -self.KNOCKBACK_DISTANCE
        )

    def _check_target_life(self, target: Union['Player', 'Mob']) -> None:
        # Verifica se a vida da entidade chegou a 0 e lida de acordo. 
        if target.life <= 0:
            target.defeat()
            target.kill()