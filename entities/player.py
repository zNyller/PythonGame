import pygame
from components.player_attack_component import PlayerAttackComponent
from components.basic_movement_component import BasicMovementComponent
from components.stats_bar_component import StatsBarComponent
from entities.level_manager import LevelManager

class Player(pygame.sprite.Sprite):
    """
    Uma classe para representar o jogador.

    Atributos:
        rect: Posição e tamanho do retângulo que envolverá a imagem do player
        mask: Cria uma máscara de colisão a partir da imagem do player
    """

    # Constants
    MAX_LIFE = 100
    INITIAL_STRENGTH = 1
    INITIAL_POSITION = (600, 586)
    MOVE_SPEED = 4
    SWORD_DAMAGE = 10
    ATTACK_DURATION = 65
    ATTACK_COOLDOWN = 21
    ATTACK_RANGE = 70
    INITIAL_XP = 100


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
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION)
        self.mask = pygame.mask.from_surface(self.image)

        # Atributos de combate
        self.attack_damage = self.SWORD_DAMAGE + self.strength
        self.attack_duration = self.ATTACK_DURATION
        self.attack_cooldown = self.ATTACK_COOLDOWN
        self.attack_range = self.ATTACK_RANGE
        self.attack_sound = sounds["attacking"]
        self.receive_damage_sound = sounds["hit"]
        self.death_sound = sounds["game_over"]
        #self.attack_component = BasicAttackComponent(self, self.attack_damage, self.attack_duration, self.attack_range, self.attack_sound, self.attack_cooldown, self.event_manager)
        self.attack_component = PlayerAttackComponent(self, self.attack_damage, self.attack_duration, self.attack_sound, self.event_manager)
        self.stats_bar_component = StatsBarComponent(self, images['stats_interface'], images['life_bar'], images['xp_bar'])
        # Movimento
        self.movement_component = BasicMovementComponent(self.rect, self.speed, self.event_manager)

        self.level_manager = LevelManager(self)
        self.event_manager.subscribe('mob_defeated', self)

        # Tempo de animação
        self.animation_speed = 0.1
        self.animation_counter = 0


    def update(self, mobs_sprites):
        """Atualiza o estado do jogador"""
        
        self.update_animation()
        self.handle_events()
        self.attack_component.update()
        self.movement_component.update(self.rect)
        #self.attack_component.update(mobs_sprites)


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
        """Desenha a barra de vida do jogador."""
        self.stats_bar_component.draw_stats_bar(screen)
        

    def handle_events(self):
        """Lida com os eventos do jogador, como ataques."""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack_component.attack()

    # Encapsulando o acesso à life (@property é usado para definir o método 'life' como uma propriedade da classe Player.
    @property
    def life(self):
        """Aqui, o método life é uma propriedade somente leitura.
        Quando você acessar player.life, irá retornar o valor atual de self._life"""
        return self._life
    

    @life.setter
    def life(self, value):
        """@life.setter define um método life que é chamado quando você tenta definir o valor de player.life. 
        self._life = max(0, value) garante que a vida do jogador não se torne negativa."""
        self._life = max(0, value)


    def reduce_life(self, damage):
        """Método para reduzir a vida."""
        self.life -= damage


    def reset(self):
        """Reseta a posição e vida do jogador."""

        self.rect.center = self.INITIAL_POSITION
        self._life = self.MAX_LIFE


    def on_mob_defeated(self):
        self.level_manager.add_experience(10)
        print(f"+10XP! Total: {self.level_manager.xp}")


    def notify(self, event):
        if event['type'] == 'mob_defeated':
            self.on_mob_defeated()


    def upgrade_stats(self, attack_range, strength):
        self.attack_range += attack_range
        self.strength += strength