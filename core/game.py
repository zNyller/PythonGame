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
    """Classe principal. Coordena o ciclo do jogo. 
    
    É responsável pela inicialização, atualização e exibição dos elementos do jogo. 
    """
    
    FPS = 60
    MAP_WIDTH = 3072
    MAP_HEIGHT = 768
    FIXED_DELTA_TIME = 0.016

    def __init__(self) -> None:
        """Inicializa a biblioteca pygame e os componentes do jogo."""
        pygame.init()
        self._running = False
        self._menu = False
        self._initialize_managers()
        self._initialize_factories()
        self._initialize_entities()

    def _initialize_managers(self) -> None:
        """Inicializa os gerenciadores do loop principal."""
        self._screen_manager = ScreenManager()
        self._resource_manager = ResourceManager()
        self._event_manager = EventManager()
        self._sprite_manager = SpriteManager(self._resource_manager, self._event_manager)
        self._camera = Camera(
            width=self._screen_manager.screen.get_width(), 
            height=self._screen_manager.screen.get_height(), 
            map_width=self.MAP_WIDTH, 
            map_height=self.MAP_HEIGHT
        )

    def _initialize_factories(self) -> None:
        """Inicializa as fábricas de entidades."""
        self._player_factory = PlayerFactory(
            self._event_manager, 
            self._resource_manager, 
            self._sprite_manager
        )
        self._mob_factory = MobFactory(
            self._event_manager, 
            self._resource_manager, 
            self._sprite_manager
        )

    def _initialize_entities(self) -> None:
        """Cria as entidades iniciais do jogo."""
        self._player = self._player_factory.create_player()
        self._mob_factory.create_mob("Soul")
        self._mob_factory.create_mob("Troll")

    def menu(self):
        """Inicia o menu do jogo."""
        self._menu = True

    def run(self) -> None:
        """Inicia o ciclo principal do jogo."""
        self._running = True
        try:
            while self._running:
                self._game_loop()
        except Exception as e:
            self._handle_exception(e)
        finally:
            pygame.quit()

    def _game_loop(self) -> None:
        """Executa o ciclo do loop principal do jogo chamando os métodos correspondentes."""
        self._screen_manager.clock.tick(self.FPS)
        self._handle_events()
        self._update(self.FIXED_DELTA_TIME)
        self._draw()

    def _handle_events(self) -> None:
        """Lida com os eventos do jogo/resposta de comandos."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Lida com as teclas pressionadas chamando suas respectivas funções."""
        if event.key == pygame.K_r:
            self._sprite_manager.reset_game()

    def _update(self, delta_time: float) -> None:
        """Atualiza os sprites e a câmera."""
        self._sprite_manager.update_all(delta_time)
        self._camera.update(self._player)

    def _draw(self) -> None:
        """Desenha os elementos do jogo e atualiza a tela."""
        self._screen_manager.draw_window(self._resource_manager, self._camera)
        self._sprite_manager.draw_all(self._screen_manager.screen, self._camera)
        pygame.display.flip()

    def _handle_exception(self, e: Exception, **kwargs) -> None:
        """Trata diferentes tipos de exceções e fornece logs detalhados."""
        if isinstance(e, pygame.error):
            print(f"Erro do Pygame: {e}")
        elif isinstance(e, FileNotFoundError):
            print(f"Arquivo não encontrado: {e}")
        elif isinstance(e, AttributeError):
            print(f"Erro de atributo: {e}")
        else:
            print(f"Erro inesperado: {e}")
        traceback.print_exc() # Imprime a pilha de chamadas completa para depuração