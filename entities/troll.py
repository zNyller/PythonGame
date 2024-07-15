import pygame

from entities.mob import Mob
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY, RED
from components.basic_animation_component import BasicAnimationComponent
from components.basic_attack_component import BasicAttackComponent
from components.life_bar_component import LifeBarComponent
from components.mob_movement_component import MobMovementComponent

class Troll(Mob, pygame.sprite.Sprite):
    """
    Entidade inimiga que representa um Mob "Troll" no jogo.

    Configura atributos específicos como vida, força, velocidade, e comportamentos como movimento e ataques.

    Utiliza métodos da classe Mob para gerenciar comportamentos genéricos de entidades.
    """

    MAX_LIFE = 60
    STRENGTH = 25
    INITIAL_POSITION = (2150, 550)
    MOVE_SPEED = 120 # 120
    ATTACK_RANGE = 200
    XP_POINTS = 20
    ATTACK_DURATION = 20
    ATTACK_SPEED = 5


    def __init__(self, name, images, sounds, event_manager) -> None:
        super().__init__(event_manager)
        self.name = name
        self.images = images
        self.sounds = sounds
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp_points = self.XP_POINTS
        self.initial_position = self.INITIAL_POSITION
        self.type = 'Troll'
        self.initialize_image_attributes()
        self.initialize_combat_attributes()
        self.initialize_components()


    def initialize_image_attributes(self) -> None:
        """ Inicializa os atributos de imagem do Soul.

        Define as imagens padrão e de ataque e posiciona o mob na tela.
        """
        self.default_frames = self.images['idle_frames']
        self.attack_frames = self.images['idle_frames']
        self.image = self.default_frames[0]
        self.rect = self.image.get_rect(center=self.INITIAL_POSITION)


    def initialize_combat_attributes(self) -> None:
        """ Inicializa os atributos de combate. """
        self.receive_damage_sound = self.sounds['pain']
        self.death_sound = self.sounds['death']
        self.strength = self.STRENGTH
        self.attack_duration = self.ATTACK_DURATION
        self.attack_speed = self.ATTACK_SPEED


    def initialize_components(self) -> None:
        """ Inicializa os componentes utilizados por Troll. """
        self.animation_component = BasicAnimationComponent(
            entity=self, 
            animation_frames=self.default_frames, 
            event_manager=self.event_manager
        )
        self.attack_component = BasicAttackComponent(
            entity=self, 
            damage=self.STRENGTH, 
            attack_duration=self.ATTACK_DURATION, 
            attack_range=self.ATTACK_RANGE, 
            attack_sound=self.sounds, 
            event_manager=self.event_manager
        )
        self.life_bar_component = LifeBarComponent(
            entity=self, 
            event_manager=self.event_manager, 
            width=50, 
            height=8, 
            color=RED
        )
        self.move_component = MobMovementComponent(
            mob=self,
            attack_component=self.attack_component,
            event_manager=self.event_manager
        )


    def update(self, delta_time) -> None:
        """ Atualiza a direção, o movimento, os ataques e a barra de vida do mob. """
        super().update(delta_time)