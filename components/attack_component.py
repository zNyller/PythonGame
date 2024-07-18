from abc import ABC, abstractmethod

class AttackComponent(ABC):
    """Classe abstrata para componentes de ataque.

    Define a interface que todos os componentes de ataque devem implementar.
    """

    ATTACK_STATE = 'attacking'
    IDLE_STATE = 'idle'
    KNOCKBACK_DISTANCE = 90

    def __init__(self, entity) -> None:
        self.entity = entity
        self.state = self.IDLE_STATE

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def update(self, target_sprites):
        pass

    @abstractmethod
    def _perform_attack(self, target_sprites):
        pass

    @abstractmethod
    def _reset_attack(self):
        pass

    def inflict_damage(self, target, damage: int) -> None:
        """Inflige dano ao alvo e verifica a vida restante."""
        target.receive_damage(damage)
        self._check_target_life(target)

    def knockback_target(self, target) -> None:
        """Aplica efeito de recuo no alvo com base na sua posição."""
        target.rect.centerx += (
            self.KNOCKBACK_DISTANCE if target.rect.centerx > self.entity.rect.centerx 
            else -self.KNOCKBACK_DISTANCE
        )

    def _check_target_life(self, target) -> None:
        # Verifica se a vida da entidade chegou a 0 e lida de acordo. 
        if target.life <= 0:
            target.defeat()
            target.kill()