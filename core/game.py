# Imports
import pygame
import traceback

# Imports internos
from managers.screen_manager import ScreenManager
from managers.resource_manager import ResourceManager
from managers.event_manager import EventManager
from managers.sprite_manager import SpriteManager
from core.camera import Camera
from entities.player_factory import PlayerFactory
from entities.mob_factory import MobFactory

class Game:
    """ Classe principal do jogo. Coordena a inicialização, atualização e exibição dos elementos do jogo. """
    
    FPS = 60
    MAP_WIDTH = 3072
    MAP_HEIGHT = 768
    FIXED_DELTA_TIME = 0.016


    def __init__(self) -> None:
        """ Inicializa a biblioteca pygame e os componentes do jogo. """
        pygame.init()
        self._initialize_managers()
        self._initialize_factories()
        self._initialize_entities()
        self.running = False


    def _initialize_managers(self) -> None:
        """ Inicializa os gerenciadores do loop principal. """
        self.screen_manager = ScreenManager()
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.sprite_manager = SpriteManager(
            resource_manager=self.resource_manager, 
            event_manager=self.event_manager
        )
        self.camera = Camera(
            width=self.screen_manager.screen.get_width(), 
            height=self.screen_manager.screen.get_height(), 
            map_width=self.MAP_WIDTH, 
            map_height=self.MAP_HEIGHT
        )


    def _initialize_factories(self) -> None:
        """ Inicializa as fábricas de entidades. """
        self.player_factory = PlayerFactory(
            event_manager=self.event_manager, 
            resource_manager=self.resource_manager, 
            sprite_manager=self.sprite_manager
        )
        self.mob_factory = MobFactory(
            event_manager=self.event_manager, 
            resource_manager=self.resource_manager, 
            sprite_manager=self.sprite_manager
        )


    def _initialize_entities(self) -> None:
        """ Cria as entidades iniciais do jogo. """
        self.player = self.player_factory.create_player()
        self.mob_factory.create_mob(name="Soul")
        self.mob_factory.create_mob(name="Troll")


    def run(self) -> None:
        """ Inicia o ciclo principal do jogo. """
        self.running = True
        try:
            while self.running:
                self._game_loop()
        except Exception as e:
            self._handle_exception(e)
        finally:
            pygame.quit()


    def _game_loop(self) -> None:
        """ Executa o ciclo do loop principal do jogo chamando os métodos correspondentes. """
        self.screen_manager.clock.tick(self.FPS)
        self._handle_events()
        self._update(self.FIXED_DELTA_TIME)
        self._draw()


    def _handle_events(self) -> None:
        """ Lida com os eventos do jogo/resposta de comandos. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)


    def _handle_keydown(self, event) -> None:
        """ Lida com as teclas pressionadas chamando suas respectivas funções. """
        if event.key == pygame.K_r:
            self.sprite_manager.reset_game()
    

    def _update(self, delta_time: float) -> None:
        """ Atualiza os sprites e a câmera. """
        self.sprite_manager.update_all(delta_time)
        self.camera.update(self.player)


    def _draw(self) -> None:
        """ Desenha os elementos do jogo e atualiza a tela. """
        self.screen_manager.draw_window(self.resource_manager, self.camera)
        self.sprite_manager.draw_all(self.screen_manager.screen, self.camera)
        pygame.display.flip()


    def _handle_exception(e: Exception, **kwargs) -> None:
        """ Trata diferentes tipos de exceções e fornece logs detalhados. """
        if isinstance(e, pygame.error):
            print(f"Erro do Pygame: {e}")
        elif isinstance(e, FileNotFoundError):
            print(f"Arquivo não encontrado: {e}")
        elif isinstance(e, AttributeError):
            print(f"Erro de Atributo: {e}")
        else:
            print(f"Erro inesperado: {e}")
        traceback.print_exc() # Imprime a pilha de chamadas completa para depuração