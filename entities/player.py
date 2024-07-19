import pygame

from managers.event_manager import EventManager
from components.animation.basic_animation_component import BasicAnimationComponent
from components.attack.player_atk_component import PlayerAttackComponent
from components.movement.basic_movement_component import BasicMovementComponent
from components.stats_bar_component import StatsBarComponent
from entities.level_manager import LevelManager

class Player(pygame.sprite.Sprite):
    """ Uma classe para representar o jogador. """

    MAX_LIFE = 100
    INITIAL_POSITION = (200, 515)
    INITIAL_STRENGTH = 1
    ANIMATION_SPEED = 7
    MOVE_SPEED = 360
    SWORD_DAMAGE = 20
    SPECIAL_DAMAGE = 30

    def __init__(self, images: dict, sounds: dict, event_manager: EventManager) -> None:
        """ Inicializa um novo jogador e configura seus atributos. """ 
        super().__init__()
        self.name = 'Guts'
        self.images = images
        self.sounds = sounds
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.INITIAL_STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp = 0
        self._initialize_image_attributes()
        self._initialize_combat_attributes()
        self._initialize_components()

    def _initialize_image_attributes(self) -> None:
        """Inicializa os atributos de imagem do Player."""
        self.idle_frames = self.images['default']
        self.attack_frames = self.images['attacking']
        self.cannon_frames = self.images['cannon']
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION)

    def _initialize_combat_attributes(self) -> None:
        """Inicializa os atributos de combate do Player."""
        self._attack_damage = self.SWORD_DAMAGE + self.strength
        self.cannon_damage = self.SPECIAL_DAMAGE
        self.attack_sound = self.sounds["attacking"]
        self.attack_sound_2 = self.sounds["attacking2"]
        self.cannon_sound = self.sounds["cannon"]
        self.receive_damage_sound = self.sounds["hit"]
        self.death_sound = self.sounds["game_over"]
        self.up_sound = self.sounds["level_complete"]

    def _initialize_components(self) -> None:
        """Inicializa os components utilizados pelo Player."""
        self.attack_component = PlayerAttackComponent(
            player=self, 
            sounds={
                'attack_sound': self.attack_sound, 
                'attack_sound_2': self.attack_sound_2, 
                'cannon_sound': self.cannon_sound
            }, 
            event_manager=self.event_manager
        )
        self.stats_bar_component = StatsBarComponent(
            player=self, 
            interface=self.images['stats_interface'], 
            life_bar=self.images['life_bar'],
            xp_bar=self.images['xp_bar'], 
            event_manager=self.event_manager
        )
        self.movement_component = BasicMovementComponent(
            entity_rect=self.rect, 
            movement_speed=self.speed, 
            event_manager=self.event_manager
        )
        self.animation_component = BasicAnimationComponent(
            entity=self, 
            animation_frames=self.idle_frames,
            event_manager=self.event_manager
        )
        self.level_manager = LevelManager(self, self.event_manager)

    def draw_stats_bar(self, screen: pygame.Surface) -> None:
        """ Desenha a barra de stats do jogador. """
        self.stats_bar_component.draw_stats_bar(screen)

    def update(self, delta_time: float) -> None:
        """ Atualiza o estado do jogador. """
        self.animation_component.update(delta_time)
        self.handle_events()
        self._update_components(delta_time)

    def handle_events(self) -> None:
        """ Lida com os eventos do jogador, como ataques. """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack_component.attack(1)
        if keys[pygame.K_LCTRL]:
            self.attack_component.attack(2)

    def receive_damage(self, damage: int) -> None:
        """ Reduz a vida do player e notifica os listeners. """
        self.life -= damage
        self.receive_damage_sound.play()
        self.event_manager.notify(
            event={'type': 'damage_event', 'target': self, 'damage': damage}
        )

    def defeat(self) -> None:
        """ Lida com os efeitos de game over. """
        self.death_sound.play()

    def reset(self) -> None:
        """ Reseta a posição e vida do jogador. """
        self.rect.center = self.INITIAL_POSITION
        self._life = self.MAX_LIFE

    def _update_components(self, delta_time: float) -> None:
        """ Atualiza os componentes do player. """
        self.attack_component.update(delta_time)
        self.movement_component.update(self.rect, delta_time)

    @property
    def life(self) -> int:
        """ Retorna o valor atual da vida do jogador. """
        return self._life

    @life.setter
    def life(self, value: int) -> None:
        """ Define o valor da vida do jogador. """
        self._life = max(0, value)

    @property
    def attack_damage(self) -> int:
        """ Retorna o dano de ataque atual do jogador. """
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value: int) -> None:
        """ Define o valor do dano de ataque do jogador. """
        self._attack_damage = max(0, value)