class LevelManager:
    def __init__(self, player, event_manager):
        self.player = player
        self.level = 1
        self.xp_to_next_level = 100
        self.upgrade_points = 0
        self.event_manager = event_manager

        self.event_manager.subscribe('mob_defeated', self)


    def add_experience(self, amount):
        self.player.xp += amount
        if self.player.xp >= self.xp_to_next_level:
            self.level_up()


    def level_up(self):
        self.level += 1
        self.player.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.upgrade_points += 1
        self.apply_upgrades()


    def apply_upgrades(self):
        if self.upgrade_points > 0:
            self.player.attack_damage += 3
            self.upgrade_points -= 1


    def notify(self, event):
        if event['type'] == 'mob_defeated':
            self.add_experience(event['xp_points'])