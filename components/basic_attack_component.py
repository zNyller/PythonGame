import pygame
from components.attack_component import AttackComponent

class BasicAttackComponent(AttackComponent):
    """
    Componente de ataque para as entidade do jogo.

    Este componente gerencia o estado de ataque da entidade, incluindo a duração,
    a aplicação de dano aos alvos atingidos e a reprodução de sons de ataque.
    """

    def __init__(self, entity, damage, attack_duration, attack_range, attack_sound, attack_cooldown, event_manager):
        self.entity = entity
        self.attack_damage = damage
        self.initial_attack_duration = self.attack_duration = attack_duration
        self.attack_range = attack_range
        self.attack_sound = attack_sound
        self.initial_attack_cooldown = self.attack_cooldown = attack_cooldown
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


    def update(self, target_sprites):
        """Atualiza o estado de ataque e cooldown."""

        if self.state == 'attacking':
            if self.attack_duration > 0:
                self._perform_attack(target_sprites)
                self.attack_duration -= 1
            else:
                self.reset_attack_state()
                self.state = 'cooldown'
                self.attack_cooldown = self.initial_attack_cooldown # Reseta o cooldown
        elif self.state == 'cooldown':
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            else:
                self.state = 'idle'


    def _perform_attack(self, target_sprites):
        for target in target_sprites:
            # Verifica a colisão apenas se o centro do mob estiver perto do centro do jogador
            mob_center = self.entity.rect.center
            player_center = target.rect.center
            collision_distance = 158  # Define a distância máxima para considerar a colisão

            if self.is_within_attack_range(mob_center, player_center, collision_distance):
                if target not in self.hit_targets:
                    self.entity.image = self.entity.attacking_image
                    self.attack_sound.play()
                    self._inflict_damage(target)
                    self.hit_targets.add(target)

    def is_within_attack_range(self, mob_center, player_center, collision_distance):
        return (abs(mob_center[0] - player_center[0]) <= collision_distance and
                abs(mob_center[1] - player_center[1]) <= collision_distance)


    def _inflict_damage(self, target):
        """ Inflige dano ao alvo e lida com os eventos relativos. """

        target.reduce_life(self.attack_damage)
        target.receive_damage_sound.play()

        # Notifica a barra de vida sobre a mudança
        self.event_manager.notify({
            'type': 'damage_event',
            'target': target,
            'damage': self.attack_damage
        })
        
        self._knock_back_target(target)
        self._check_target_life(target)


    def _knock_back_target(self, target):
        """ Calcula a direção do recuo com base nas posições do atacante e do alvo. """
        if target.rect.centerx >= self.entity.rect.centerx:
            self.entity.rect.centerx -= 90
        else:
            self.entity.rect.centerx += 90


    def _check_target_life(self, target):
        """ Verifica se a vida do alvo chegou a 0 e lida de acordo. """
        if target.life <= 0:
            target.death_sound.play()
            target.kill()


    def reset_attack_state(self):
        """Retorna a imagem da entidade à sua imagem padrão."""
        
        self.entity.image = self.entity.default_image