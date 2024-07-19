import pygame

from entities.mob import Mob
from config.constants import RED
from components.animation.basic_animation_component import BasicAnimationComponent
from components.attack.basic_atk_component import BasicAttackComponent
from components.life_bar_component import LifeBarComponent
from components.movement.mob_movement_component import MobMovementComponent

class Troll(Mob, pygame.sprite.Sprite):
    """Entidade inimiga que representa um Mob "Troll" no jogo.

    Configura atributos específicos como vida, força, velocidade, e comportamentos como movimento e ataques.
    Utiliza métodos da classe Mob para gerenciar comportamentos genéricos de entidades.
    """

    MAX_LIFE = 60
    STRENGTH = 25
    INITIAL_POSITION = (2150, 535)
    MOVE_SPEED = 140
    ATTACK_RANGE = 200
    XP_POINTS = 20
    ATTACK_DURATION = 20
    ATTACK_SPEED = 5

    def __init__(self, name, images, sounds, event_manager) -> None:
        """Inicializa os atributos específicos do Troll."""
        super().__init__(event_manager)
        self._name = name
        self._images = images
        self._sounds = sounds
        self._event_manager = event_manager
        self._initial_position = self.INITIAL_POSITION
        self._life = self.MAX_LIFE
        self._strength = self.STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp_points = self.XP_POINTS
        self.type = 'Troll'
        self.initialize_image_attributes()
        self.initialize_combat_attributes()
        self.initialize_components()

    def initialize_image_attributes(self) -> None:
        """Inicializa os atributos de imagem do Troll.

        Define as imagens padrão e de ataque e posiciona o mob na tela.
        """
        self.default_frames = self._images['idle_frames']
        self.attack_frames = self._images['idle_frames']
        self.image = self.default_frames[0]
        self.rect = self.image.get_rect(center=self._initial_position)

    def initialize_combat_attributes(self) -> None:
        """Inicializa os atributos de combate do Troll."""
        self.receive_damage_sound = self._sounds['pain']
        self.death_sound = self._sounds['death']

    def initialize_components(self) -> None:
        """Inicializa os componentes utilizados por Troll."""
        self.animation_component = BasicAnimationComponent(
            entity=self, 
            animation_frames=self.default_frames, 
            event_manager=self._event_manager
        )
        self.attack_component = BasicAttackComponent(
            entity=self, 
            damage=self._strength, 
            attack_duration=self.ATTACK_DURATION, 
            attack_range=self.ATTACK_RANGE, 
            attack_sound=self._sounds, 
            event_manager=self._event_manager
        )
        self.life_bar_component = LifeBarComponent(
            entity=self, 
            event_manager=self._event_manager, 
            width=50, 
            height=8, 
            color=RED
        )
        self.movement_component = MobMovementComponent(
            mob=self,
            attack_component=self.attack_component,
            event_manager=self._event_manager
        )

    def update(self, delta_time: float) -> None:
        """Atualiza a direção, o movimento, os ataques e a barra de vida do mob."""
        super().update(delta_time)
        self.animation_component.update(delta_time)