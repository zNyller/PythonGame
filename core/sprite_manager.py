import pygame

class SpriteManager:
    """Gerencia os sprites do jogo."""

    PLAYER_SPRITE_COORDS = [
        (0, 0, 280, 148),    # Sprite 1 (1ª linha, 1ª coluna)
        (280, 0, 280, 148),  # Sprite 2 (1ª linha, 2ª coluna)
        (0, 148, 280, 148),  # Sprite 3 (2ª linha, 1ª coluna)
        (280, 148, 280, 148),# Sprite 4 (2ª linha, 2ª coluna)
        (0, 296, 280, 148),  # Sprite 5 (3ª linha, 1ª coluna)
    ]

    ATTACK_SPRITE_COORDS = [
        (245, 64, 244, 134), # [1/1]
        (750, 40, 244, 162), # [2/1]
        (1172, 0, 232, 200), # [3/1]
        (0, 254, 368, 142), # [1/2]
        (506, 204, 356, 196), # [2/2]
        (996, 254, 368, 142), # [3/2]
        (222, 398, 232, 200), # [1/3]
        (750, 432, 244, 162), # [2/3]
        (1244, 462, 244, 134) # [3/3]
    ]
    
    def __init__(self, resource_manager, event_manager):
        self.event_manager = event_manager
        self.resource_manager = resource_manager

        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()

        self.player_sprite_coords = self.PLAYER_SPRITE_COORDS
        self.attack_sprite_coords = self.ATTACK_SPRITE_COORDS

        self.subscribe_to_events()


    def subscribe_to_events(self):
        self.event_manager.subscribe('get_mob_sprites', self)


    def add_player(self, player):
        """Adiciona aos grupos de sprites."""

        self.player_sprites.add(player)
        self.all_sprites.add(player)


    def add_mob(self, mob):
        """Adiciona um mob ao grupo de mobs e grupo de todos os sprites"""

        self.mob_sprites.add(mob)
        self.all_sprites.add(mob)
    

    def update_all(self):
        """Atualiza os sprites na tela."""

        self.player_sprites.update()
        self.mob_sprites.update(self.player_sprites)


    def draw_all(self, screen):
        """Desenha os sprites e seus elementos na tela."""

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
    

    def get_mob_sprites(self):
        return self.mob_sprites
    

    def notify(self, event):
        if event['type'] == 'get_mob_sprites':
            return self.get_mob_sprites()
    

    def reset_game(self):
        """Reseta o estado das entidades e retorna um novo mob."""

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