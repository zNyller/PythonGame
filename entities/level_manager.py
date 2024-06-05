class LevelManager:
    def __init__(self, player):
        self.player = player
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.upgrade_points = 0


    def add_experience(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()


    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.upgrade_points += 1
        self.apply_upgrades()


    def apply_upgrades(self):
        if self.upgrade_points > 0:
            self.player.upgrade_stats(5, 3)
            self.player.strength += 1
            self.upgrade_points -= 1