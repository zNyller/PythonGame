import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height
        self.margin = 50


    def apply(self, entity):
        """ Aplica a câmera à entidade. """
        if hasattr(entity, 'rect'):
            return entity.rect.move(self.camera.topleft)
        return entity.move(self.camera.topleft)


    def update(self, target):
        """ Atualiza a posição da câmera com base no target. """
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limite a câmera aos limites do mapa
        x = max(min(x, 0), -(self.map_width - self.width))  # Lados esquerdo e direito
        y = max(min(y, 0), -(self.map_height - self.height))  # Parte superior e inferior

        self.camera = pygame.Rect(x, y, self.width, self.height)


    def is_visible(self, entity):
        """ Verifica se a entidade está dentro do campo de visão da câmera. """
        camera_with_margin = self.camera.inflate(self.margin * 2, self.margin * 2)
        entity_rect = entity.rect.move(self.camera.topleft)
        return camera_with_margin.colliderect(entity_rect)