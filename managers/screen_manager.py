import pygame
from managers.resource_manager import ResourceManager
from core.camera import Camera
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class ScreenManager:
    """ Gerencia e desenha a janela do jogo. """

    def __init__(self) -> None:
        """ Inicializa e configura a janela e o relógio do jogo. """
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(title="Slayer")
        self.clock = pygame.time.Clock()

    def draw_window(
            self: "ScreenManager", 
            resource_manager: ResourceManager, 
            camera: Camera
        ) -> None:
        """ Desenha a janela e a imagem de fundo. """
        self.screen.fill(color=BLACK)
        background = resource_manager.get_image('background')
        self.screen.blit(background, (camera.camera.x, camera.camera.y))