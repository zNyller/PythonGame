import pygame
from components.player_attack_component import PlayerAttackComponent
from components.basic_movement_component import BasicMovementComponent
from components.stats_bar_component import StatsBarComponent
from entities.level_manager import LevelManager

class Player(pygame.sprite.Sprite):
    """ Uma classe para representar o jogador. """

    # Constants
    INITIAL_STRENGTH = 1
    INITIAL_POSITION = (600, 586)
    INITIAL_XP = 0
    MAX_LIFE = 100
    MOVE_SPEED = 6
    SWORD_DAMAGE = 10


    def __init__(self, images, sounds, event_manager):
        super().__init__()
        """Inicializa um novo jogador e configura seus atributos.""" 

        self.name = 'Guts'
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.INITIAL_STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp = self.INITIAL_XP

        # Imagem e posição
        self.animation_state = 'default' # Estado de animação inicial
        self.animation_frames = images['default'] # Conjunto de frames de animação
        self.attack_frames = images['attacking'] # Conjunto de frames de ataque
        self.current_frame_index = 0 # Índice atual do frame de animação
        self.image = self.animation_frames[self.current_frame_index]
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION) # Posição e tamanho do retângulo que envolverá a imagem do player
        self.mask = pygame.mask.from_surface(self.image) # Máscara de colisão a partir da imagem do player

        # Atributos de combate
        self._attack_damage = self.SWORD_DAMAGE + self.strength
        self.attack_sound = sounds["attacking"]
        self.receive_damage_sound = sounds["hit"]
        self.death_sound = sounds["game_over"]

        # Components
        self.attack_component = PlayerAttackComponent(self, self.attack_sound, self.event_manager)
        self.stats_bar_component = StatsBarComponent(self, images['stats_interface'], images['life_bar'], images['xp_bar'])
        self.movement_component = BasicMovementComponent(self.rect, self.speed, self.event_manager)

        self.level_manager = LevelManager(self, self.event_manager)

        # Tempo de animação
        self.animation_speed = 0.15
        self.animation_counter = 0


    def update(self):
        """Atualiza o estado do jogador"""
        
        self.update_animation()
        self.handle_events()
        self.attack_component.update()
        self.movement_component.update(self.rect)
        print(self.rect)


    def update_animation(self):
        """Atualiza a animação do sprite"""
        if self.animation_state == 'default':
            self.animation_counter += self.animation_speed
            if self.animation_counter >= len(self.animation_frames):
                self.animation_counter = 0
            self.current_frame_index = int(self.animation_counter)
            self.image = self.animation_frames[self.current_frame_index]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=self.rect.center)


    def draw_stats_bar(self, screen):
        """ Desenha a barra de stats do jogador. """
        self.stats_bar_component.draw_stats_bar(screen)
        

    def handle_events(self):
        """ Lida com os eventos do jogador, como ataques. """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack_component.attack()


    @property
    def life(self):
        """ Retorna o valor atual da vida do jogador.
        @property define o método 'life' como uma propriedade somente leitura. 
        Quando você acessa player.life, ele retorna o valor atual de self._life. """
        return self._life


    @life.setter
    def life(self, value):
        """ Define o valor da vida do jogador.

        @life.setter permite definir o valor da vida do jogador quando você tenta atribuir um novo valor a player.life.

        Args:
            value (int): Novo valor da vida do jogador.

        Nota:
            self._life = max(0, value) garante que a vida do jogador não seja definida como um valor negativo.
            Se value for menor que 0, self._life será definido como 0.

        Exemplo:
            player.life = 50  # Define a vida do jogador como 50.
        """
        self._life = max(0, value)


    def reduce_life(self, damage):
        """Método para reduzir a vida."""
        self.life -= damage


    @property
    def attack_damage(self):
        """ Retorna o dano de ataque atual do jogador. """
        return self._attack_damage
    

    @attack_damage.setter
    def attack_damage(self, value):
        """ Define o valor do dano de ataque do jogador. """
        self._attack_damage = max(0, value)


    def reset(self):
        """Resetar a posição e vida do jogador."""

        self.rect.center = self.INITIAL_POSITION
        self._life = self.MAX_LIFE