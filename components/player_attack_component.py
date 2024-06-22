import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):

    ATTACK_DURATION = 44

    def __init__(self, player, sound, event_manager):
        super().__init__()
        self.player = player
        self.attack_duration = self.ATTACK_DURATION
        self.sound = sound
        self.event_manager = event_manager
        self.state = 'idle'
        self.animation_speed = 0.20
        self.animation_counter = 0
        self.current_frame_index = 0
        self.duration_counter = 0
        self.initial_rect = player.rect.copy()
        self.attack_hitbox = pygame.Rect(0, 0, 50, 50)
        self.hit_targets = set()


    def attack(self):
        """ Inicia o ataque se estiver inativo e notifica os listeners. """
        if self.state == 'idle':
            print(self.player.rect.x)
            self.state = 'attacking'
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self.duration_counter = self.attack_duration
            self.sound.play()
            self._reset_attack_hitbox()
            self._update_player_image()
            self._update_attack_hitbox()


    def update(self):
        """ Atualiza o estado de ataque. """
        if self.state == 'attacking':
            self._continue_attack()


    def _continue_attack(self):
        """ Gerencia a animação de ataque. """
        if self.duration_counter > 0:
            self._attack_animation()
            self._perform_attack()
            self.duration_counter -= 1
        else:
            self._reset_to_idle()


    def _reset_to_idle(self):
        """ Reseta o estado de ataque para inativo e notifica os listeners. """
        self.state = 'idle'
        self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
        self.animation_counter = 0
        self.current_frame_index = 0
        self.duration_counter = 0
        self.hit_targets.clear()


    def _perform_attack(self):
        """ Verifica a colisão com alvos e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_mob_sprites'})
        for target in target_sprites:
            if self.attack_hitbox.colliderect(target.rect) and target not in self.hit_targets:
                self._inflict_damage(target)
                self.hit_targets.add(target)


    def _inflict_damage(self, target):
        """ Inflige dano ao alvo e lida com os eventos relativos. """
        self.damage = self.player.attack_damage
        print(f"Inflicting {self.damage} damage on target")
        target.reduce_life(self.damage)
        target.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': target, 'damage': self.damage})
        self._knockback_target(target)
        self._check_target_life(target)


    def _knockback_target(self, target):
        """ Aplica efeito de recuo no alvo com base na posição do player. """
        if target.rect.centerx <= self.player.rect.centerx:
            print(f'Direta! Target: {target.rect.centerx}! Player: {self.player.rect.centerx}')
            target.rect.centerx -= 90
        else:
            print(f'Esquerda! Target: {target.rect.centerx}! Player: {self.player.rect.centerx}')
            target.rect.centerx += 90


    def _check_target_life(self, target):
        """ Verifica se a vida do alvo chegou a zero e lida de acordo. """
        if target.life <= 0:
            target.death_sound.play()
            target.kill()
            if hasattr(target, 'xp_points'):
                self.event_manager.notify({
                    'type': 'mob_defeated', 
                    'xp_points': target.xp_points
                })


    def _attack_animation(self):
        """ Avança os frames da animação de ataque. """
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.player.attack_frames)
            self._update_attack_hitbox()
        self._update_player_image()


    def _update_player_image(self):
        """ Atualiza a imagem do player com base no frame de ataque atual. """
        self.player.image = self.player.attack_frames[self.current_frame_index]
        self.player.rect = self.player.image.get_rect()
        self.player.rect.centerx = self.initial_rect.centerx
        self.player.rect.bottom = self.initial_rect.bottom


    def _update_attack_hitbox(self):
        """ Atualiza a hitbox de ataque com base no frame atual. """
        if self.current_frame_index < 3:
            self.attack_hitbox.size = (50, 50)
        elif 3 <= self.current_frame_index < 6:
            self.attack_hitbox.size = (330, 250)
        else:
            self.attack_hitbox.size = (50, 50)
        self.attack_hitbox.centerx = self.player.rect.centerx
        self.attack_hitbox.bottom = self.player.rect.bottom


    def _reset_attack_hitbox(self):
        """ Reseta a hitbox do ataque com base na posição do player. """
        self.attack_hitbox = pygame.Rect(self.player.rect.centerx - 25, self.player.rect.bottom - 50, 50, 50)