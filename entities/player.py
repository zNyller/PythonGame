import pygame
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY, GREEN
from components.basic_attack_component import BasicAttackComponent
from components.basic_movement_component import BasicMovementComponent
from components.life_bar_component import LifeBarComponent

class Player(pygame.sprite.Sprite):
    """
    Uma classe para representar o jogador.

    Atributos:
        rect: Posição e tamanho do retângulo que envolverá a imagem do player
        mask: Cria uma máscara de colisão a partir da imagem do player
        attack_damage (int): Variável para configurar a força do ataque do player
        attack_duration (int): Variável para definir a duração do ataque
    """

    # Constants
    MAX_LIFE = 100
    INITIAL_STRENGTH = 1
    INITIAL_POSITION = (380, 363)
    MOVE_SPEED = 4
    SWORD_DAMAGE = 10
    ATTACK_DURATION = 20
    ATTACK_COOLDOWN = 21


    def __init__(self, name, images, sounds, event_manager):
        super().__init__()
        """ Inicializa um novo jogador com um nome settavel, vida, fome e força padrões. 

        Raises:
            ValueError: Se o nome do jogador não for uma string válida.
        """
        if not isinstance(name, str): raise ValueError("O nome do jogador deve ser uma string!")

        self.name = name
        self.event_manager = event_manager
        self._life = self.MAX_LIFE
        self.strength = self.INITIAL_STRENGTH
        self.speed = self.MOVE_SPEED

        # Imagem e posição
        self.default_image = images['default']
        self.attacking_image = images['attacking']
        self.image = self.default_image
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION)
        self.mask = pygame.mask.from_surface(self.image)

        # Barra de vida
        self.life_bar_component = LifeBarComponent(self, event_manager, width=40, height=8, color=GREEN)

        # Atributos de combate
        self.attack_damage = self.SWORD_DAMAGE + self.strength
        self.attack_duration = self.ATTACK_DURATION
        self.attack_cooldown = self.ATTACK_COOLDOWN
        self.attack_sound = sounds["attacking"]
        self.attack_component = BasicAttackComponent(self, self.attack_damage, self.attack_duration, self.attack_sound, self.attack_cooldown, self.event_manager)
        
        # Movimento
        self.movement_component = BasicMovementComponent(self.rect, self.speed)


    def update(self, mobs_sprites):
        """Atualiza o estado do jogador"""
        
        self.handle_events()
        self.life_bar_component.update_life_bar()
        self.movement_component.handle_movements()
        self.movement_component.limits_movements(LEFT_BOUNDARY, RIGHT_BOUNDARY)
        self.attack_component.update(mobs_sprites)


    def draw_life_bar(self, screen):
        """Desenha a barra de vida do jogador."""

        self.life_bar_component.draw_life_bar(screen)
        

    def handle_events(self):
        """Lida com os eventos do jogador, como ataques."""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.attack_component.attack()


    def reset(self):
        """Reseta a posição e vida do jogador."""

        self.rect.center = self.INITIAL_POSITION
        self._life = self.MAX_LIFE


    # Encapsulando o acesso à life (@property é usado para definir o método 'life' como uma propriedade da classe Player.)
    @property
    def life(self):
        """Aqui, o método life é uma propriedade somente leitura.
        Quando você acessar player.life, ele irá retornar o valor atual de self._life"""
        return self._life
    

    @life.setter
    def life(self, value):
        """@life.setter define um método life que é chamado quando você tenta definir o valor de player.life. 
        self._life = max(0, value) garante que a vida do jogador não se torne negativa."""
        self._life = max(0, value)


    def reduce_life(self, damage):
        """Método para reduzir a vida."""
        self.life -= damage