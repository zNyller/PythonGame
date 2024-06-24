import pygame
from components.player_attack_component import PlayerAttackComponent
from components.basic_movement_component import BasicMovementComponent
from components.stats_bar_component import StatsBarComponent
from entities.level_manager import LevelManager

class Player(pygame.sprite.Sprite):
    """ Uma classe para representar o jogador. """

    # Constants
    ANIMATION_SPEED = 0.15
    INITIAL_STRENGTH = 1
    INITIAL_POSITION = (600, 586)
    MAX_LIFE = 100
    MOVE_SPEED = 6
    SWORD_DAMAGE = 50


    def __init__(self, images, sounds, event_manager) -> None:
        """ Inicializa um novo jogador e configura seus atributos. """ 
        super().__init__()

        self.name = 'Guts'
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.INITIAL_STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp = 0

        # Imagem e posição
        self.animation_state = 'default' # Estado de animação inicial
        self.animation_frames = images['default'] # Conjunto de frames de animação
        self.attack_frames = images['attacking'] # Conjunto de frames de ataque
        self.cannon_frames = images['cannon']
        self.current_frame_index = 0 # Índice atual do frame de animação
        self.image = self.animation_frames[self.current_frame_index]
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION) # Posição e tamanho do retângulo que envolverá a imagem do player
        self.mask = pygame.mask.from_surface(self.image) # Máscara de colisão a partir da imagem do player

        # Atributos de combate
        self._attack_damage = self.SWORD_DAMAGE + self.strength
        self.attack_sound = sounds["attacking"]
        self.receive_damage_sound = sounds["hit"]
        self.death_sound = sounds["game_over"]
        self.up_sound = sounds["level_complete"]

        # Components
        self.attack_component = PlayerAttackComponent(self, self.attack_sound, self.event_manager)
        self.stats_bar_component = StatsBarComponent(self, images['stats_interface'], images['life_bar'], images['xp_bar'], self.event_manager)
        self.movement_component = BasicMovementComponent(self.rect, self.speed, self.event_manager)

        self.level_manager = LevelManager(self, self.event_manager)

        # Tempo de animação
        self.animation_speed = self.ANIMATION_SPEED
        self.animation_counter = 0


    def draw_stats_bar(self, screen) -> None:
        """ Desenha a barra de stats do jogador. """
        self.stats_bar_component.draw_stats_bar(screen)


    def update(self) -> None:
        """ Atualiza o estado do jogador. """
        
        self._update_animation()
        self.handle_events()
        self._update_components()


    def handle_events(self) -> None:
        """ Lida com os eventos do jogador, como ataques. """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack_component.attack()


    def receive_damage(self, damage) -> None:
        """ Reduz a vida do player e notifica os listeners. """
        self.life -= damage
        self.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': self, 'damage': damage})


    def reset(self) -> None:
        """ Reseta a posição e vida do jogador. """
        self.rect.center = self.INITIAL_POSITION
        self._life = self.MAX_LIFE


    def _update_animation(self) -> None:
        """ Atualiza a animação do sprite. """
        if self.animation_state == 'default':
            self._increment_animation_counter()
            self._update_current_frame()
            self._update_image_and_mask()


    def _increment_animation_counter(self) -> None:
        """ Incrementa o contador de animação. """
        self.animation_counter += self.animation_speed
        if self.animation_counter >= len(self.animation_frames):
            self.animation_counter = 0


    def _update_current_frame(self) -> None:
        """ Atualiza o frame atual da animação. """
        self.current_frame_index = int(self.animation_counter)


    def _update_image_and_mask(self) -> None:
        """ Atualiza a imagem e a máscara do sprite. """
        self.image = self.animation_frames[self.current_frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)


    def _update_components(self) -> None:
        """ Atualiza os componentes do player. """
        self.attack_component.update()
        self.movement_component.update(self.rect)


    @property
    def life(self) -> int:
        """ Retorna o valor atual da vida do jogador. """
        return self._life


    @life.setter
    def life(self, value) -> None:
        """ Define o valor da vida do jogador. """
        self._life = max(0, value)


    @property
    def attack_damage(self) -> int:
        """ Retorna o dano de ataque atual do jogador. """
        return self._attack_damage
    

    @attack_damage.setter
    def attack_damage(self, value) -> None:
        """ Define o valor do dano de ataque do jogador. """
        self._attack_damage = max(0, value)