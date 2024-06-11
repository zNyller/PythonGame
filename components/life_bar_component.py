import pygame
from config import constants

class LifeBarComponent:
    """
    Calcula a posição e dimensões da barra de vida com base no status do jogador ou entidade.
    Desenha a barra de vida na tela.
    """
    def __init__(self, entity, event_manager, width, height, color):
        self.entity = entity
        self.width = width
        self.height = height
        self.color = color

        self.max_life = entity.life
        self.current_life = entity.life
        self.entity_rect = entity.rect
        self.previous_life = entity.life

        self.outline = self.create_life_bar(self.entity_rect.centerx, self.entity_rect.top, self.width, self.height)
        self.inner = self.create_life_bar(self.entity_rect.centerx, self.entity_rect.top, self.width, self.height)

        self.event_manager = event_manager
        self.event_manager.subscribe('damage_event', self)


    def notify(self, event):
        """Recebe notificações de eventos."""
        if event['type'] == 'damage_event' and event['target'] == self.entity:
            self.update_life_bar()


    def create_life_bar(self, centerx, top, width, height):
        """Cria e retorna a barra de vida utilizando as medidas apropriadas."""

        return pygame.Rect(centerx - width // 2, top -5, width, height)


    def draw_life_bar(self, screen):
        """Desenha a barra de vida na tela."""

        pygame.draw.rect(screen, self.color, self.inner)
        # Contorno da barra 
        pygame.draw.rect(screen, constants.WHITE, self.outline, 2)


    def update_life_bar(self):
        """Atualiza a barra de vida da entidade quando houver alteração."""
        self.current_life = self.entity.life

        if self.max_life > 0:
            # Verifica se houve alteração na vida
            if self.previous_life != self.current_life:
                # Calcula a largura proporcional da barra interna
                self.inner.width = int(self.width * (self.current_life / self.max_life))
                self.previous_life = self.current_life
        else:
            self.inner.width = 0

        # Atualiza a posição da barra de vida junto com a posição da entidade
        self.outline.centerx = self.entity_rect.centerx
        self.inner.centerx = self.entity_rect.centerx
        self.outline.top = self.entity_rect.top -5
        self.inner.top = self.entity_rect.top -5