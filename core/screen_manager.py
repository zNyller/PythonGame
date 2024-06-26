import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class ScreenManager:
    def __init__(self):
        """ Gerencia a janela e o relógio do jogo. """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Slayer")
        self.clock = pygame.time.Clock()


    def draw_game(self, resource_manager, camera):
        """Desenha a janela e a imagem de fundo com efeito contínuo."""
        self.screen.fill(BLACK)
        background = resource_manager.get_image('background')
        bg_width = background.get_width()
        bg_height = background.get_height()

        # Desenhar o fundo de forma contínua
        for x in range(-bg_width, SCREEN_WIDTH + bg_width, bg_width):
            for y in range(-bg_height, SCREEN_HEIGHT + bg_height, bg_height):
                self.screen.blit(background, (x + camera.camera.x % bg_width, y + camera.camera.y % bg_height))