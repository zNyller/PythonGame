import pygame
from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY, RED
from components.life_bar_component import LifeBarComponent
from components.basic_attack_component import BasicAttackComponent

class Mob(pygame.sprite.Sprite):
    """ Uma classe para representar os mobs do jogo.

    Atributos:
        life (int): Pontos de vida do mob
        strength (int): Pontos de força do mob para ataque
        image (Surface): Imagem do mob
        rect (Rect): Retângulo de colisão do mob
        mask (Mask): Máscara de colisão do mob
        receive_damage_sound (Sound): Som de dano recebido pelo mob
        death_sound (Sound): Som de morte do mob
    """

    MAX_LIFE = 50
    STRENGTH = 15
    INITIAL_POSITION = (150, 520)
    MOVE_SPEED = 1.5
    ATTACK_RANGE = 65
    XP_POINTS = 40


    def __init__(self, name, images, sounds, event_manager):
        super().__init__()
        # Atributos gerais
        self.name = name
        self.images = images
        self.sounds = sounds
        self._life = self.MAX_LIFE
        self.strength = self.STRENGTH
        self.speed = self.MOVE_SPEED
        self.xp_points = self.XP_POINTS

        # Imagem e posição
        self.default_image = images["default"]
        self.attacking_image = images["attacking"]
        self.image = self.default_image
        self.rect = self.image.get_rect(center = self.INITIAL_POSITION) 
        self.mask = pygame.mask.from_surface(self.image)

        self.event_manager = event_manager
        # Barra de vida
        self.life_bar_component = LifeBarComponent(self, event_manager, width=40, height=8, color=RED)
        # Atributos de combate
        self.attack_range = self.ATTACK_RANGE
        self.attack_component = BasicAttackComponent(self, self.strength, 25, self.attack_range, sounds["hit_player"], 30, self.event_manager)
        self.receive_damage_sound = sounds["scream"]
        self.death_sound = sounds["blood_pop"]


    def reset(self):
        """Reseta o mob para seu estado inicial padrão e emite o evento de reset."""

        self._life = self.MAX_LIFE
        self.rect.center = self.INITIAL_POSITION

        event = {'type': 'mob_reset', 'target': self}
        self.event_manager.notify(event)


    def draw_life_bar(self, screen):
        self.life_bar_component.draw_life_bar(screen)


    def update(self, player_sprites):
        """ Atualiza a posição da barra de vida e verifica colisão com o player para mover. """

        self.life_bar_component.update_life_bar()
        self.attack_component.update(player_sprites)
        self._check_colision(player_sprites)


    def defeat(self):
        """ Efeito de morte e notifica os listeners. """
        self.death_sound.play()
        self.event_manager.notify({'type': 'mob_defeated', 'xp_points': self.xp_points})


    def _check_colision(self, player_sprites):
        hit_player = pygame.sprite.spritecollideany(self, player_sprites, pygame.sprite.collide_mask)
        if not hit_player:
            self._move()
        elif self.attack_component.state == 'idle':
            self.attack_component.attack()


    def _move(self):
        """ Move o mob e limita o movimento dentro das bordas. """
        self.rect.x += self.speed
        if self.rect.left < LEFT_BOUNDARY or self.rect.right > RIGHT_BOUNDARY:
            self.rect.center = self.INITIAL_POSITION


    @property
    def life(self):
        return self._life
    

    @life.setter
    def life(self, value):
        self._life = max(0, value)


    def receive_damage(self, damage):
        """ Recebe a quantidade de dano e notifica os listeners. """
        self.life -= damage
        self.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': self, 'damage': damage})