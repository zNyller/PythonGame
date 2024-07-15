import pygame
import math
from entities.mob import Mob
from config.constants import RED
from components.life_bar_component import LifeBarComponent
from components.basic_attack_component import BasicAttackComponent
from components.mob_movement_component import MobMovementComponent

class Soul(Mob, pygame.sprite.Sprite):
    """Entidade inimiga que representa um Mob "Soul" no jogo.

    Configura atributos específicos como vida, força, velocidade, e comportamentos como
    movimento, ataques e efeitos visuais de flutuação.

    Utiliza métodos da classe Mob para gerenciar comportamentos genéricos de entidades.
    """

    MAX_LIFE = 50
    STRENGTH = 15
    MOVE_SPEED = 150
    INITIAL_POSITION = (1150, 480)
    ATTACK_RANGE = 365
    ATTACK_DURATION = 25
    XP_POINTS = 20
    FLOAT_AMPLITUDE = 10
    FLOAT_SPEED = 6


    def __init__(self, name: str, images: dict, sounds: dict, event_manager) -> None:
        """ Inicializa os atributos específicos para Soul. """
        super().__init__(event_manager)
        self.name = name
        self.images = images
        self.sounds = sounds
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp_points = self.XP_POINTS
        self.initialize_image_attributes()
        self.initialize_combat_attributes()
        self.initialize_components()


    def initialize_image_attributes(self) -> None:
        """ Inicializa os atributos de imagem do Soul.

        Define as imagens padrão e de ataque, posiciona o mob na tela e configura parâmetros
        visuais como amplitude e velocidade de flutuação.
        """

        self.default_frames = self.images["default"]
        self.attacking_image = self.images["attacking"]
        self.image = self.default_frames
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION) 
        self.float_amplitude = self.FLOAT_AMPLITUDE
        self.float_speed = self.FLOAT_SPEED
        self.float_offset = 0


    def initialize_combat_attributes(self) -> None:
        """ Inicializa os atributos de combate. """
        self.receive_damage_sound = self.sounds["scream"]
        self.death_sound = self.sounds["blood_pop"]


    def initialize_components(self) -> None:
        """ Inicializa os componentes utilizados por Mob. """
        self.attack_component = BasicAttackComponent(
            entity=self, 
            damage=self.STRENGTH, 
            attack_duration=self.ATTACK_DURATION, 
            attack_range=self.ATTACK_RANGE, 
            attack_sound=self.sounds["hit_player"], 
            event_manager=self.event_manager
        )
        self.life_bar_component = LifeBarComponent(
            entity=self, 
            event_manager=self.event_manager, 
            width=60, 
            height=8, 
            color=RED
        )
        self.move_component = MobMovementComponent(
            mob=self,
            attack_component=self.attack_component,
            event_manager=self.event_manager
        )


    def update(self, delta_time) -> None:
        """ Atualiza a direção, o movimento, os ataques, a barra de vida e a flutuação do mob. """
        super().update(delta_time)
        self._update_float(delta_time)


    def _update_float(self, delta_time) -> None:
        """ Atualiza a posição y do mob para criar um efeito de flutuação. """
        self.float_offset += self.float_speed * delta_time
        float_y = self.INITIAL_POSITION[1] + self.float_amplitude * math.sin(self.float_offset)
        self.rect.y = int(float_y)
        self.life_bar_component.update_life_bar()