import pygame

class SpriteManager:
    """Gerencia os sprites do jogo."""

    PLAYER_SPRITE_COORDS = [
        (5, 8, 290, 148),    # Sprite 1 (1ª linha, 1ª coluna)
        (302, 6, 290, 150),  # Sprite 2 (1ª linha, 2ª coluna)
        (5, 162, 290, 152),  # Sprite 3 (2ª linha, 1ª coluna)
        (300, 164, 290, 150),# Sprite 4 (2ª linha, 2ª coluna)
        (5, 324, 290, 148),  # Sprite 5 (3ª linha, 1ª coluna)
    ]

    ATTACK_SPRITE_COORDS = [
        (272, 70, 270, 150), # [1/1] 
        (830, 40, 270, 180), # [2/1] 
        (1300, 0, 255, 222), # [3/1]
        (0, 280, 398, 156), # [1/2]
        (562, 226, 394, 218), # [2/2]
        (1105, 280, 398, 156), # [3/2]
        (248, 442, 255, 222), # [1/3]
        (830, 480, 270, 180), # [2/3]
        (1378, 512, 270, 150) # [3/3]
    ]

    CANNON_ATTACK_COORDS = [
        (386, 188, 298, 151), # [1/1]
        (1196, 186, 298, 154), # [2/1]
        (2016, 162, 298, 178), # [3/1]
        (2820, 162, 318, 178), # [4/1]
        (376, 620, 334, 168), # [1/2]
        (1180, 624, 339, 168), # [2/2]
        (1992, 624, 339, 168), # [3/2]
        (2800, 624, 341, 168), # [4/2]
        (375, 1078, 339, 160), # [1/3]
        (1184, 1079, 339, 160), # [2/3]
        (2007, 1079, 324, 160), # [3/3]
        (2816, 1078, 324, 160), # [4/3]
        (389, 1530, 324, 159), # [1/4]
        (1198, 1530, 324, 159), # [2/4]
        (2009, 1530, 324, 159), # [3/4]
        (2728, 1516, 462, 165), # [4/4]
        (300, 1977, 460, 165), # [1/5]
        (1052, 1971, 537, 162), # [2/5]
        (1863, 1977, 537, 162), # [3/5]
        (2630, 1924, 582, 216), # [4/5]
        (194, 2367, 603, 225), # [1/6]
        (948, 2367, 663, 225), # [2/6]
        (1738, 2364, 681, 228), # [3/6]
        (2529, 2372, 696, 216), # [4/6]
        (74, 2829, 716, 210), # [1/7]
        (861, 2825, 746, 212), # [2/7]
        (1646, 2827, 771, 210), # [3/7]
        (2445, 2819, 723, 216), # [4/7]
        (9, 3260, 684, 226), # [1/8]
        (822, 3258, 678, 231), # [2/8]
        (1629, 3256, 675, 231), # [3/8]
        (2817, 3338, 297, 150), # [4/8]
    ]
    
    def __init__(self, resource_manager, event_manager):
        self.event_manager = event_manager
        self.resource_manager = resource_manager

        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()

        self.player_sprite_coords = self.PLAYER_SPRITE_COORDS
        self.attack_sprite_coords = self.ATTACK_SPRITE_COORDS
        self.cannon_attack_coords = self.CANNON_ATTACK_COORDS

        self.subscribe_to_events()


    def subscribe_to_events(self):
        self.event_manager.subscribe('get_mob_sprites', self)
        self.event_manager.subscribe('get_player_sprites', self)


    def add_player(self, player):
        """ Adiciona aos grupos de sprites. """

        self.player_sprites.add(player)
        self.all_sprites.add(player)


    def add_mob(self, mob):
        """ Adiciona um mob ao grupo de mobs e grupo de todos os sprites. """
        self.mob_sprites.add(mob)
        self.all_sprites.add(mob)
    

    def update_all(self):
        """ Atualiza os sprites na tela. """

        self.player_sprites.update()
        self.mob_sprites.update()


    def draw_all(self, screen):
        """ Desenha os sprites e seus elementos na tela. """

        for entity in self.all_sprites:
            if hasattr(entity, 'draw_stats_bar'):
                entity.draw_stats_bar(screen)
            else:
                entity.draw_life_bar(screen)

            screen.blit(entity.image, entity.rect)


    def get_sprite(self, spritesheet, x, y, width, height):
        """ Retorna uma superfície (sprite) recortada do spritesheet nas coordenadas (x, y). """
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(spritesheet, (0, 0), (x, y, width, height))
        return sprite
    

    def get_player_sprites(self):
        return self.player_sprites
    

    def get_mob_sprites(self):
        return self.mob_sprites
    

    def notify(self, event):
        if event['type'] == 'get_mob_sprites':
            return self.get_mob_sprites()
        elif event['type'] == 'get_player_sprites':
            return self.get_player_sprites()
    

    def reset_game(self):
        """ Reseta o estado das entidades e retorna um novo mob. """
        self._reset_player()
        self._release_mob()
        return self._get_new_mob()
    

    def _reset_player(self):
        if not self.player_sprites:
            self.event_manager.notify({'type': 'create_player'})
        else:
            for player in self.player_sprites:
                player.reset()


    def _release_mob(self):
        for mob in self.mob_sprites:
            self.event_manager.notify({'type': 'release_mob', 'mob': mob})
            mob.kill()


    def _get_new_mob(self):
        new_mob = self.event_manager.notify({'type': 'get_mob', 'name': 'New Demon'})
        return new_mob