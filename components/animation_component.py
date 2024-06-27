import pygame

class AnimationComponent:
    """ Gerencia a animação da entidade. """

    DEFAULT_STATE = 'default'

    def __init__(self, entity, animation_frames, animation_speed) -> None:
        self.entity = entity
        self.animation_frames = animation_frames
        self.animation_speed = animation_speed
        self.animation_state = self.DEFAULT_STATE
        self.current_frame_index = 0 
        self.animation_counter = 0
        self.last_frame_index = -1  # Rastrear quando a imagem realmente muda


    def update(self, delta_time):
        if self.animation_state == self.DEFAULT_STATE:
            """ Incrementa o contador de animação. """
            self._increment_animation_counter(delta_time)
            self._update_current_frame()
            self._update_image_and_mask()


    def _increment_animation_counter(self, delta_time):
        self.animation_counter += self.animation_speed * delta_time
        if self.animation_counter >= len(self.animation_frames):
            self.animation_counter = 0


    def _update_current_frame(self):
        """ Atualiza a imagem e a máscara do sprite. """
        self.current_frame_index = int(self.animation_counter)


    def _update_image_and_mask(self):
        """ Atualiza a imagem e a máscara do sprite. """
        if self.current_frame_index != self.last_frame_index:
            self.entity.image = self.animation_frames[self.current_frame_index]
            if self.entity.movement_component.facing_right:
                self.entity.image = pygame.transform.flip(self.entity.image, True, False)
            self.mask = pygame.mask.from_surface(self.entity.image)
            self.rect = self.entity.image.get_rect(center=self.entity.rect.center)