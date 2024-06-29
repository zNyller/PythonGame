import pygame

from entities.mob import Mob
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY, RED
from components.animation_component import AnimationComponent
from components.basic_attack_component import BasicAttackComponent
from components.life_bar_component import LifeBarComponent

class Troll(pygame.sprite.Sprite):
    """ Gerencia o mob "Troll". """

    MAX_LIFE = 50
    STRENGTH = 25
    INITIAL_POSITION = (2150, 480)
    MOVE_SPEED = 150
    ATTACK_RANGE = 200
    XP_POINTS = 20
    ANIMATION_SPEED = 0.1
    ATTACK_DURATION = 20
    ATTACK_SPEED = 5


    def __init__(self, name, images, sounds, event_manager) -> None:
        super().__init__()
        self.name = name
        self.images = images
        self.sounds = sounds
        self.event_manager = event_manager
        self.life = self.MAX_LIFE
        # Imagem
        self.idle_frames = images['idle_frames']
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=self.INITIAL_POSITION)
        self._direction = 1  # 1 for right, -1 for left
        # Combate
        self.strength = self.STRENGTH
        self.attack_duration = self.ATTACK_DURATION
        self.attack_speed = self.ATTACK_SPEED
        # Components
        self.animation_component = AnimationComponent(self, self.idle_frames, self.event_manager)
        self.attack_component = BasicAttackComponent(self, self.strength, self.attack_duration, self.ATTACK_RANGE, 
                                                     sounds, self.event_manager)
        self.life_bar_component = LifeBarComponent(self, self.event_manager, width=50, height=8, color=RED)



    def draw_life_bar(self, screen, camera) -> None:
        self.life_bar_component.draw_life_bar(screen, camera)
    

    def update(self, delta_time) -> None:
        previous_direction = self._direction
        self.attack_component.update()
        if self._direction != previous_direction:
            self.image = pygame.transform.flip(self.image, True, False)


    def _handle_collision(self, delta_time) -> None:
        """ Verifica se houve colisão com o player e lida de acordo. """
        if self._has_collided():
            self.attack_component.attack()
        else: self._move(delta_time)


    def _has_collided(self) -> bool:
        """ Verifica colisão com o jogador considerando uma distância mínima. """
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for target in player_sprites:
                distance_threshold = 150  # Distância mínima para considerar colisão
                if abs(self.rect.centerx - target.rect.centerx) <= distance_threshold:
                    return True
        return False
    

    def _move(self, delta_time):
        """ Move o mob e limita o movimento dentro das bordas. """
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for player in player_sprites:
                if self.rect.centerx <= player.rect.centerx:
                    self._direction = 1
                    self.rect.x += self.speed * delta_time
                else:
                    self._direction = -1
                    self.rect.x -= self.speed * delta_time
        if self.rect.left < LEFT_BOUNDARY or self.rect.right > RIGHT_BOUNDARY:
            self.rect.center = self.INITIAL_POSITION


    def reset(self) -> None:
        """ Reseta o mob para seu estado inicial padrão e emite o evento de reset. """
        self.life = self.MAX_LIFE
        self.rect.center = self.INITIAL_POSITION
        self.event_manager.notify({'type': 'mob_reset', 'target': self})
