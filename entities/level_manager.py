from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player
    from managers.event_manager import EventManager

class LevelManager:
    """Gerencia o sistema de niveis do Player."""

    LEVEL = 1
    XP_TO_NEXT_LEVEL = 100

    def __init__(self, player: 'Player', event_manager: 'EventManager') -> None:
        self.player = player
        self._event_manager = event_manager
        self._level = self.LEVEL
        self._xp_to_next_level = self.XP_TO_NEXT_LEVEL
        self._upgrade_points = 0
        self._event_manager.subscribe('mob_defeated', self)

    def add_experience(self, amount: int) -> None:
        """Adiciona xp e verifica se atingiu o próximo nível."""
        self.player.xp += amount
        if self.player.xp >= self._xp_to_next_level:
            self._level_up()

    def _level_up(self) -> None:
        """Aumenta o nível do jogador e notifica os listeners."""
        self._level += 1
        self._upgrade_points += 1
        self.player.xp -= self._xp_to_next_level
        self._xp_to_next_level = int(self._xp_to_next_level * 1.5)
        self._event_manager.notify({'type': 'player_up'})
        self.apply_upgrades()

    def apply_upgrades(self) -> None:
        """Verifica se há _upgrade_points para aplicar as melhorias."""
        if self._upgrade_points > 0:
            self.player.attack_damage += 3
            self._upgrade_points -= 1
            self.player.up_sound.play()
            print(f'New level! Strength +3')

    def notify(self, event: dict) -> None:
        """Chama os métodos inscritos no tipo do evento recebido."""
        if event['type'] == 'mob_defeated':
            self.add_experience(event['xp_points'])