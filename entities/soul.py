import pygame
import math
from typing import Any, Dict, TYPE_CHECKING
from entities.mob import Mob
from config.constants import RED
from components.life_bar_component import LifeBarComponent
from components.attack.basic_atk_component import BasicAttackComponent
from components.movement.mob_movement_component import MobMovementComponent

if TYPE_CHECKING:
    from managers.event_manager import EventManager

class Soul(Mob, pygame.sprite.Sprite):
    """Entidade inimiga que representa um Mob "Soul" no jogo.

    Configura atributos específicos como vida, força, velocidade, e comportamentos como
    movimento, ataques e efeitos visuais de flutuação.

    Utiliza métodos da classe Mob para gerenciar comportamentos genéricos de entidades.
    """

    MAX_LIFE = 50
    STRENGTH = 15
    MOVE_SPEED = 150
    INITIAL_POSITION = (1150, 465)
    ATTACK_RANGE = 365
    ATTACK_DURATION = 25
    XP_POINTS = 20
    FLOAT_AMPLITUDE = 10
    FLOAT_SPEED = 6

    def __init__(
            self, name: str, 
            images: Dict[str, Any], 
            sounds: Dict[str, Any], 
            event_manager: 'EventManager'
        ) -> None:
        """ Inicializa os atributos específicos para Soul. """
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
        self.type = 'Soul'
        self.initialize_image_attributes()
        self.initialize_combat_attributes()
        self.initialize_components()

    def initialize_image_attributes(self) -> None:
        """Inicializa os atributos de imagem do Soul.

        Define as imagens padrão e de ataque, posiciona o mob na tela e configura parâmetros
        visuais como amplitude e velocidade de flutuação.
        """
        self.default_image = self._images["default"]
        self.attack_image = self._images["attacking"]
        self.image = self.default_image
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION) 
        self._float_amplitude = self.FLOAT_AMPLITUDE
        self._float_speed = self.FLOAT_SPEED
        self._float_offset = 0

    def initialize_combat_attributes(self) -> None:
        """Inicializa os atributos de combate."""
        self.receive_damage_sound = self._sounds["scream"]
        self.death_sound = self._sounds["blood_pop"]

    def initialize_components(self) -> None:
        """Inicializa os componentes utilizados por Soul."""
        self.attack_component = BasicAttackComponent(
            entity=self, 
            damage=self.STRENGTH, 
            attack_duration=self.ATTACK_DURATION, 
            attack_range=self.ATTACK_RANGE, 
            attack_sound=self._sounds["hit_player"], 
            event_manager=self._event_manager
        )
        self.life_bar_component = LifeBarComponent(
            entity=self, 
            event_manager=self._event_manager, 
            width=60, 
            height=8, 
            color=RED
        )
        self.movement_component = MobMovementComponent(
            mob=self,
            attack_component=self.attack_component,
            event_manager=self._event_manager
        )

    def update(self, delta_time: float) -> None:
        """Atualiza a direção, o movimento, os ataques, a barra de vida e a flutuação do mob."""
        super().update(delta_time)
        self._update_float(delta_time)

    def _update_float(self, delta_time: float) -> None:
        # Atualiza a posição 'y' do mob para criar um efeito de flutuação.
        self._float_offset += self._float_speed * delta_time
        self.rect.y = int(
            self.INITIAL_POSITION[1] + self._float_amplitude * math.sin(self._float_offset)
        )
        self.life_bar_component.update_life_bar()