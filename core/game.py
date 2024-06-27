# Imports
import pygame

# Imports internos
from managers.screen_manager import ScreenManager
from managers.resource_manager import ResourceManager
from managers.event_manager import EventManager
from managers.sprite_manager import SpriteManager
from core.camera import Camera
from entities.player_factory import PlayerFactory
from entities.mob_factory import MobFactory

class Game:
    """ Classe principal do jogo. """
    
    FPS = 60
    MAP_WIDTH = 3072
    MAP_HEIGHT = 768

    def __init__(self):
        pygame.init()
        self.screen_manager = ScreenManager()
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.sprite_manager = SpriteManager(self.resource_manager, self.event_manager)
        self.camera = Camera(self.screen_manager.screen.get_width(), self.screen_manager.screen.get_height(), self.MAP_WIDTH, self.MAP_HEIGHT)
        self.player_factory = PlayerFactory(self.event_manager, self.resource_manager, self.sprite_manager)
        self.mob_factory = MobFactory(self.event_manager, self.resource_manager, self.sprite_manager)
        self.player = self.player_factory.create_player()
        self.mob = self.mob_factory.create_mob("Demon")


    def run(self) -> None:
        """ Loop principal do jogo. """
        self.running = True
        try:
            while self.running:
                delta_time = self.screen_manager.clock.tick(self.FPS) / 1000.0
                self._handle_events()
                self._update(delta_time)
                self._draw()
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            pygame.quit()


    def _handle_events(self) -> None:
        """ Lida com os eventos do jogo/resposta de comandos. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)


    def _handle_keydown(self, event):
        if event.key == pygame.K_r:
            self.sprite_manager.reset_game()
    

    def _update(self, delta_time: float) -> None:
        """ Atualiza os elementos na tela. """
        self.sprite_manager.update_all(delta_time)
        self.camera.update(self.player)


    def _draw(self) -> None:
        """ Desenha os elementos do jogo e atualiza a tela. """
        self.screen_manager.draw_game(self.resource_manager, self.camera)
        self.sprite_manager.draw_all(self.screen_manager.screen, self.camera)
        pygame.display.flip()