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
    XP_POINTS = 20


    def __init__(self, name, images, sounds, event_manager) -> None:
        super().__init__()
        # Atributos gerais
        self.name = name
        self.images = images
        self.sounds = sounds
        self.event_manager = event_manager
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
        # Atributos de combate
        self.attack_range = self.ATTACK_RANGE
        self.receive_damage_sound = sounds["scream"]
        self.death_sound = sounds["blood_pop"]
        # Components
        self.attack_component = BasicAttackComponent(self, self.strength, 25, self.attack_range, sounds["hit_player"], self.event_manager)
        self.life_bar_component = LifeBarComponent(self, event_manager, width=40, height=8, color=RED)


    def draw_life_bar(self, screen) -> None:
        self.life_bar_component.draw_life_bar(screen)


    def update(self) -> None:
        """ Atualiza a posição da barra de vida e verifica colisão com o player para mover. """
        self.life_bar_component.update_life_bar()
        self.attack_component.update()
        self._check_colision()


    def receive_damage(self, damage) -> None:
        """ Recebe a quantidade de dano e notifica os listeners. """
        self.life -= damage
        self.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': self, 'damage': damage})


    def defeat(self) -> None:
        """ Efeito de morte e notifica os listeners. """
        self.death_sound.play()
        self.event_manager.notify({'type': 'mob_defeated', 'xp_points': self.xp_points})


    def reset(self) -> None:
        """ Reseta o mob para seu estado inicial padrão e emite o evento de reset. """
        self._life = self.MAX_LIFE
        self.rect.center = self.INITIAL_POSITION
        self.event_manager.notify({'type': 'mob_reset', 'target': self})


    def _check_colision(self) -> None:
        """ Verifica se houve colisão com o player e lida de acordo. """
        if not self.has_collided():
            self._move()
        elif self.attack_component.state == 'idle':
            self.attack_component.attack()


    def has_collided(self) -> bool:
        """ Verifica colisão com o jogador considerando uma margem. """
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for target in player_sprites:
                margin = 15
                player_hitbox = pygame.Rect(target.rect.x + margin, target.rect.y + margin,
                                            target.rect.width + 2 * margin, target.rect.height + 2 * margin)
                
                if self.rect.colliderect(player_hitbox):
                    return True
        return False


    def _move(self) -> None:
        """ Move o mob e limita o movimento dentro das bordas. """
        self.rect.x += self.speed
        if self.rect.left < LEFT_BOUNDARY or self.rect.right > RIGHT_BOUNDARY:
            self.rect.center = self.INITIAL_POSITION


    @property
    def life(self) -> int:
        """ Getter para o valor de life do mob. """
        return self._life
    

    @life.setter
    def life(self, value) -> None:
        """ Setter para o valor de life do mob. """
        self._life = max(0, value)