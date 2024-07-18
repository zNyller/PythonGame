from managers.event_manager import EventManager

class LevelManager:
    """Gerencia o sistema de niveis do Player."""

    LEVEL = 1
    XP_TO_NEXT_LEVEL = 100

    def __init__(self, player, event_manager: EventManager) -> None:
        self.player = player
        self.event_manager = event_manager
        self.level = self.LEVEL
        self.xp_to_next_level = self.XP_TO_NEXT_LEVEL
        self.upgrade_points = 0
        self.event_manager.subscribe('mob_defeated', self)

    def add_experience(self, amount: int) -> None:
        """Adiciona xp e verifica se atingiu o próximo nível."""
        self.player.xp += amount
        if self.player.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self) -> None:
        """Aumenta o nível do jogador e notifica os listeners."""
        self.level += 1
        self.upgrade_points += 1
        self.player.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.event_manager.notify({'type': 'player_up'})
        self.apply_upgrades()

    def apply_upgrades(self) -> None:
        """Verifica se há upgrade_points para aplicar as melhorias."""
        if self.upgrade_points > 0:
            self.player.attack_damage += 3
            self.upgrade_points -= 1
            self.player.up_sound.play()
            print(f'New level! Strength +3')

    def notify(self, event: dict) -> None:
        """Chama os métodos inscritos no tipo do evento recebido."""
        if event['type'] == 'mob_defeated':
            self.add_experience(event['xp_points'])