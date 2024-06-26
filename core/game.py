# Imports
import pygame

# Imports do projeto
from core.screen_manager import ScreenManager
from core.resource_manager import ResourceManager
from core.event_manager import EventManager
from core.sprite_manager import SpriteManager
from entities.player_factory import PlayerFactory
from entities.mob_factory import MobFactory
from core.camera import Camera

class Game:
    """Classe principal do jogo."""
    
    FPS = 60

    def __init__(self):
        pygame.init()
        self.screen_manager = ScreenManager()
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.sprite_manager = SpriteManager(self.resource_manager, self.event_manager)
        self.player_factory = PlayerFactory(self.event_manager, self.resource_manager, self.sprite_manager)
        self.mob_factory = MobFactory(self.event_manager, self.resource_manager, self.sprite_manager)
        self.player = self.player_factory.create_player()
        self.mob = self.mob_factory.create_mob("Demon")
        # Tamanho do mapa (3072x768) e tamanho da tela (1024x768)
        self.camera = Camera(self.screen_manager.screen.get_width(), self.screen_manager.screen.get_height(), 3072, 768)


    def run(self) -> None:
        """ Loop principal do jogo. """
        running = True
        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            pygame.quit()


    def handle_events(self) -> bool:
        """ Lida com os eventos do jogo/resposta de comandos e determina se o loop deve continuar ou encerrar. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.sprite_manager.reset_game()
        return True
    

    def update(self) -> None:
        """Atualiza os elementos na tela."""
        self.sprite_manager.update_all()
        self.camera.update(self.player)  # Atualiza a posição da câmera com base no jogador

    def draw(self) -> None:
        """Desenha os elementos e atualiza a tela."""
        self.screen_manager.draw_game(self.resource_manager, self.camera)
        self.sprite_manager.draw_all(self.screen_manager.screen, self.camera)
        pygame.display.flip()
        self.screen_manager.clock.tick(self.FPS)