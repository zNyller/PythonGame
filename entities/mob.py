import pygame
from abc import ABC, abstractmethod

class Mob(ABC, pygame.sprite.Sprite):
    """ Classe abstrata para representar e gerenciar mobs no jogo.

    Define comportamentos comuns para mobs, como movimento, 
    combate e interação com outros componentes do jogo.
    """

    def __init__(self, event_manager) -> None:
        super().__init__()
        self.event_manager = event_manager
        self._direction = 1 # 1 for left, -1 for right


    @abstractmethod
    def initialize_image_attributes(self):
        """ Inicializa os atributos de imagem do Mob. """
        pass


    @abstractmethod
    def initialize_combat_attributes(self):
        """ Inicializa os atributos de combate. """
        pass


    @abstractmethod
    def initialize_components(self):
        """ Inicializa os componentes utilizados pelo Mob. """
        pass


    def draw_life_bar(self, screen, camera) -> None:
        """ Desenha a barra de vida do mob de acordo com a posição. """
        self.life_bar_component.draw_life_bar(screen, camera)


    def update(self, delta_time) -> None:
        """ Atualiza a direção, o movimento, os ataques e a barra de vida do mob. """
        previous_direction = self._direction
        self.move_component.handle_collision(delta_time)
        self.attack_component.update()
        self.life_bar_component.update_life_bar()
        if self._direction != previous_direction:
            self.image = pygame.transform.flip(self.image, True, False)


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
        self.life = self.MAX_LIFE
        self.rect.center = self.INITIAL_POSITION
        self.event_manager.notify({'type': 'mob_reset', 'target': self})


    @property
    def life(self) -> int:
        """ Getter para o valor de life do mob. """
        return self._life
    

    @life.setter
    def life(self, value) -> None:
        """ Setter para o valor de life do mob. """
        self._life = max(0, value)


    @property
    def direction(self) -> int:
        """ Obtém o valor atual da direção do mob. """
        return self._direction
    

    @direction.setter
    def direction(self, value) -> None:
        """ Configura o novo valor da direção do mob. """
        self._direction = max(-1, value)