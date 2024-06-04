import pygame
from entities.mob_factory import MobFactory

class SpriteManager:
    """Gerencia os sprites do jogo."""
    
    def __init__(self, resource_manager, event_manager):
        self.event_manager = event_manager
        self.resource_manager = resource_manager

        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()

        self.mob_factory = MobFactory(self.event_manager, self.resource_manager, self)


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

        self.player_sprites.update(self.mob_sprites)
        self.mob_sprites.update(self.player_sprites)


    def draw_all(self, screen):
        """Desenha todos elementos na tela."""

        for entity in self.all_sprites:
            entity.draw_life_bar(screen)
        self.all_sprites.draw(screen)
    

    def reset_game(self):
        """Reseta o estado das entidades e retorna um novo mob."""

        for player in self.player_sprites:
            player.reset()

        for mob in self.mob_sprites:
            self.mob_factory.release_mob(mob) # Liberar mobs de volta ao pool
            mob.kill()

        new_mob = self.mob_factory.get_mob("New Demon") # Obter mob do pool
        return new_mob