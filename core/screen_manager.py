import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class ScreenManager:
    def __init__(self):
        """Gerencia a janela e o relógio do jogo."""
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Slayer")
        self.clock = pygame.time.Clock()


    def draw_game(self, resource_manager):
        """Desenha a janela e a imagem de fundo."""
        
        self.screen.fill(BLACK)
        self.screen.blit(resource_manager.get_image('camping'), (0, 0))