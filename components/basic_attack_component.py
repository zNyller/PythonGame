import pygame
from components.attack_component import AttackComponent

class BasicAttackComponent(AttackComponent):
    """
    Componente de ataque para as entidade do jogo.

    Este componente gerencia o estado de ataque da entidade, incluindo a duração,
    a aplicação de dano aos alvos atingidos e a reprodução de sons de ataque.
    """

    KNOCKBACK_DISTANCE = 90

    def __init__(self, entity, damage, attack_duration, attack_range, attack_sound, event_manager):
        self.entity = entity
        self.attack_damage = damage
        self.initial_attack_duration = self.attack_duration = attack_duration
        self.attack_range = attack_range
        self.attack_sound = attack_sound
        self.state = 'idle'
        self.hit_targets = set() # Armaneza alvos já atingidos durante o ataque atual
        self.event_manager = event_manager


    def attack(self):
        """
        Inicia a ação de ataque se não estiver em cooldown.
        Configura o estado de ataque e reproduz o som de ataque.
        """

        if self.state == 'idle':
            self.state = 'attacking'
            self.hit_targets.clear() # Limpa alvos atingidos no ataque anterior
            self.attack_duration = self.initial_attack_duration # Reseta a duração do ataque


    def update(self):
        """ Atualiza o estado de ataque. """
        if self.state == 'attacking':
            if self.attack_duration > 0:
                self._perform_attack()
                self.attack_duration -= 1
            else:
                self._reset_attack_state()


    def _perform_attack(self):
        """ Verifica colisão com o jogador e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        for target in target_sprites:
            if self.entity.rect.colliderect(target.rect) and target not in self.hit_targets:
                self._set_attacking_image()
                self._inflict_damage(target)
                self.hit_targets.add(target)


    def _set_attacking_image(self):
        if self.entity._direction == 1:
            self.entity.image = self.entity.attacking_image
        else:
            self.entity.image = pygame.transform.flip(self.entity.attacking_image, True, False)


    def _inflict_damage(self, target):
        """ Inflige dano ao alvo e lida com os eventos relativos. """
        target.receive_damage(self.attack_damage)
        self._knock_back_target(target)
        self._check_target_life(target)


    def _knock_back_target(self, target):
        """ Calcula a direção do recuo com base nas posições do atacante e do alvo. """
        if target.rect.centerx <= self.entity.rect.centerx:
            self.entity.rect.centerx += self.KNOCKBACK_DISTANCE
        else:
            self.entity.rect.centerx -= self.KNOCKBACK_DISTANCE


    def _check_target_life(self, target):
        """ Verifica se a vida do alvo chegou a 0 e lida de acordo. """
        if target.life <= 0:
            target.death_sound.play()
            target.kill()


    def _reset_attack_state(self):
        """ Retorna a imagem da entidade à sua imagem padrão. """
        self.entity.image = self.entity.default_image
        self.state = 'idle'