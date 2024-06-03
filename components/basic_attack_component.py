import pygame
from components.attack_component import AttackComponent
from entities.mob import Mob

class BasicAttackComponent(AttackComponent):
    """
    Componente de ataque para as entidade do jogo.

    Este componente gerencia o estado de ataque da entidade, incluindo a duração,
    a aplicação de dano aos alvos atingidos e a reprodução de sons de ataque.
    """

    def __init__(self, entity, damage, attack_duration, attack_sound, attack_cooldown, event_manager):
        self.entity = entity
        self.attack_damage = damage
        self.initial_attack_duration = self.attack_duration = attack_duration
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
            self.entity.image = self.entity.attacking_image
            self.attack_sound.play()
            self.hit_targets.clear() # Limpa alvos atingidos no ataque anterior
            self.attack_duration = self.initial_attack_duration # Reseta a duração do ataque


    def update(self, target_sprites):
        """Atualiza o estado de ataque e cooldown."""

        if self.state == 'attacking':
            if self.attack_duration > 0:
                self.perform_attack(target_sprites)
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


    def perform_attack(self, target_sprites):
        """Realiza o ataque e verifica colisões com os alvos."""

        hit_target = pygame.sprite.spritecollideany(self.entity, target_sprites, pygame.sprite.collide_mask)
        if hit_target and hit_target not in self.hit_targets:
            self.inflict_damage(hit_target)
            self.hit_targets.add(hit_target)


    def inflict_damage(self, target):
        """Inflige dano ao alvo, reproduz os respectivos sons e verifica se o alvo foi derrotado."""

        target.reduce_life(self.attack_damage)
        target.receive_damage_sound.play()

        # Notifica a barra de vida sobre a mudança
        self.event_manager.notify({
            'type': 'damage_event',
            'target': target,
            'damage': self.attack_damage
        })

        if isinstance(target, Mob):
            target.rect.centerx -= 30

        if target.life <= 0: # Usando a propriedade de vida encapsulada
            target.death_sound.play()
            target.kill()


    def reset_attack_state(self):
        """Retorna a imagem da entidade à sua imagem padrão."""
        
        self.entity.image = self.entity.default_image