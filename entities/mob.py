import pygame
import math
from abc import abstractmethod
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY, RED
from components.life_bar_component import LifeBarComponent
from components.basic_attack_component import BasicAttackComponent
from components.animation_component import AnimationComponent

class Mob(pygame.sprite.Sprite):
    """ Uma classe para gerenciar os mobs do jogo. """

    MAX_LIFE = 50
    STRENGTH = 15
    INITIAL_POSITION = (1150, 480)
    MOVE_SPEED = 150
    ATTACK_RANGE = 365
    XP_POINTS = 20
    ANIMATION_SPEED = 0.1


    def __init__(self, name: str, images: dict, sounds: dict, event_manager) -> None:
        super().__init__()
        # Atributos gerais
        self.name = name
        self.images = images
        self.sounds = sounds
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp_points = self.XP_POINTS
        # Imagem e posição
        self._init_image_atributes(images)
        # Atributos de combate
        self.attack_range = self.ATTACK_RANGE
        self.receive_damage_sound = sounds["scream"]
        self.death_sound = sounds["blood_pop"]
        # Components
        self.attack_component = BasicAttackComponent(self, self.strength, 25, self.attack_range, sounds["hit_player"], self.event_manager)
        self.life_bar_component = LifeBarComponent(self, event_manager, width=60, height=8, color=RED)
        self.animation_component = AnimationComponent(self, self.default_frames, self.event_manager)

        # Tempo de animação
        self.animation_speed = self.ANIMATION_SPEED
        self.animation_counter = 0


    def _init_image_atributes(self, images):
        self.animation_state = "default"
        self.default_frames = images["default"]
        self.attacking_image = images["attacking"]
        self.current_frame_index = 0
        self.image = self.default_frames
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION) 
        self._direction = 1  # 1 for right, -1 for left
        self.float_amplitude = 10  # Amplitude da flutuação
        self.float_speed = 6 # Velocidade da flutuação
        self.float_offset = 0  # Offset para a flutuação


    @abstractmethod
    def draw_life_bar(self, screen, camera) -> None:
        """ Desenha a barra de vida do mob de acordo com a posição. """
        self.life_bar_component.draw_life_bar(screen, camera)


    @abstractmethod
    def update(self, delta_time) -> None:
        """ Atualiza a posição da barra de vida e verifica colisão com o player para mover. """
        previous_direction = self._direction
        self._update_float(delta_time)
        self._handle_collision(delta_time)
        self.attack_component.update()
        self.life_bar_component.update_life_bar()
        if self._direction != previous_direction:
            self.image = pygame.transform.flip(self.image, True, False)


    @abstractmethod
    def receive_damage(self, damage) -> None:
        """ Recebe a quantidade de dano e notifica os listeners. """
        self.life -= damage
        self.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': self, 'damage': damage})


    def defeat(self) -> None:
        """ Efeito de morte e notifica os listeners. """
        self.death_sound.play()
        self.event_manager.notify({'type': 'mob_defeated', 'xp_points': self.xp_points})


    def reset(self) -> None:
        """ Reseta o mob para seu estado inicial padrão e emite o evento de reset. """
        self._life = self.MAX_LIFE
        self.rect.center = self.INITIAL_POSITION
        self.event_manager.notify({'type': 'mob_reset', 'target': self})


    def _update_float(self, delta_time) -> None:
        """ Atualiza a posição y do mob para criar um efeito de flutuação. """
        self.float_offset += self.float_speed * delta_time
        float_y = self.INITIAL_POSITION[1] + self.float_amplitude * math.sin(self.float_offset)
        self.rect.y = int(float_y)
        self.life_bar_component.update_life_bar()


    def _handle_collision(self, delta_time) -> None:
        """ Verifica se houve colisão com o player e lida de acordo. """
        if not self._has_collided():
            self._move(delta_time)
        elif self.attack_component.state == 'idle':
            self.attack_component.attack()


    def _has_collided(self) -> bool:
        """ Verifica colisão com o jogador considerando uma distância mínima. """
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for target in player_sprites:
                distance_threshold = 150  # Distância mínima para considerar colisão
                if abs(self.rect.centerx - target.rect.centerx) <= distance_threshold:
                    return True
        return False


    def _move(self, delta_time) -> None:
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


    @property
    def life(self) -> int:
        """ Getter para o valor de life do mob. """
        return self._life
    

    @life.setter
    def life(self, value) -> None:
        """ Setter para o valor de life do mob. """
        self._life = max(0, value)


    @property
    def direction(self) -> int:
        return self._direction