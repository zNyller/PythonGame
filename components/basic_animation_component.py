import pygame
from components.animation_component import AnimationComponent

class BasicAnimationComponent(AnimationComponent):
    """ Gerencia a animação da entidade. """

    IDLE_ANIMATION_SPEED = 7

    def __init__(self, entity, animation_frames, event_manager) -> None:
        super().__init__()
        self.entity = entity
        self.animation_frames = animation_frames
        self.event_manager = event_manager
        self.animation_speed = self.IDLE_ANIMATION_SPEED
        self.last_frame_index = -1  # Rastrear quando a imagem realmente muda


    def update(self, delta_time: float) -> None:
        """ Incrementa o contador de animação e atualiza o frame. """
        self._increment_frame_counter(delta_time)
        self._update_current_frame()
        self._update_image_and_mask()


    def _increment_frame_counter(self, delta_time: float) -> None:
        """ Incrementa o frame counter baseado na velocidade da animação e delta time"""
        self.frame_counter += self.animation_speed * delta_time
        if self.frame_counter >= len(self.animation_frames):
            self.frame_counter = 0


    def _update_current_frame(self) -> None:
        """ Atualiza o índice do frame atual baseado no frame counter. """
        self.current_frame_index = int(self.frame_counter)


    def _update_image_and_mask(self) -> None:
        """ Atualiza a imagem e a máscara do sprite. """
        if self.current_frame_index != self.last_frame_index:
            self.entity.image = self.animation_frames[self.current_frame_index]
            if self.entity.movement_component.facing_right:
                self.entity.image = pygame.transform.flip(self.entity.image, True, False)
            self.mask = pygame.mask.from_surface(self.entity.image)
            self.rect = self.entity.image.get_rect(center=self.entity.rect.center)


    def reset(self):
        pass