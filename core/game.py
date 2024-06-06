# Imports
import pygame

# Imports do projeto
from core.screen_manager import ScreenManager
from core.resource_manager import ResourceManager
from core.event_manager import EventManager
from core.sprite_manager import SpriteManager
from entities.player_factory import PlayerFactory
from entities.mob_factory import MobFactory

class Game:
    """Classe principal do jogo."""
    
    def __init__(self):
        pygame.init()
        self.screen_manager = ScreenManager()
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.sprite_manager = SpriteManager(self.resource_manager, self.event_manager)

        self.player_factory = PlayerFactory(self.event_manager, self.resource_manager, self.sprite_manager)
        self.mob_factory = MobFactory(self.event_manager, self.resource_manager, self.sprite_manager)
        self.player = self.event_manager.notify({'type': 'create_player'})
        self.mob = self.mob_factory.create_mob("Demon")


    def run(self):
        """Loop principal do jogo."""

        running = True
        while running:
            running, new_mob = self.handle_events()
            if new_mob:
                self.sprite_manager.add_mob(new_mob)
            self.update()
            self.draw()
        pygame.quit()


    def handle_events(self):
        """Lida com os eventos do jogo e resposta de comandos.
        
        Returns:
            bool: Indica se o jogo deve continuar executando (True) ou se deve ser encerrado (False).
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                new_mob = self.sprite_manager.reset_game()
                return True, new_mob
        return True, None
    

    def update(self):
        """Atualiza os elementos na tela."""
        self.sprite_manager.update_all()


    def draw(self):
        """Desenha os elementos na tela."""

        self.screen_manager.draw_game(self.resource_manager)
        self.sprite_manager.draw_all(self.screen_manager.screen)
        pygame.display.flip()
        self.screen_manager.clock.tick(60)