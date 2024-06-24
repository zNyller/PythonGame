import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):
    """ Classe para gerenciar o componente de ataque do player. """

    #ATTACK_DURATION = 44
    ATTACK_DURATION = 95
    ANIMATION_SPEED = 0.36
    STATE_IDLE = 'idle'
    STATE_ATTACKING = 'attacking'

    def __init__(self, player, sound, event_manager) -> None:
        super().__init__()
        self.player = player
        self.sound = sound
        self.event_manager = event_manager
        self.state = self.STATE_IDLE
        self.attack_duration = self.ATTACK_DURATION
        self.animation_speed = self.ANIMATION_SPEED
        self.animation_counter = 0
        self.current_frame_index = 0
        self.duration_counter = 0
        self.initial_rect = player.rect.copy()
        self.attack_hitbox = pygame.Rect(self.player.rect.centerx, self.player.rect.centery, 50, 50)
        self.hit_targets = set()


    def attack(self) -> None:
        """ Inicia o ataque se estiver inativo e notifica os listeners. """
        if self.state == self.STATE_IDLE:
            self.state = self.STATE_ATTACKING
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self.duration_counter = self.attack_duration
            self.sound.play()
            self._update_player_image()
            self._update_attack_hitbox()


    def update(self) -> None:
        """ Atualiza a posição do player e o estado de ataque. """
        self.player_x = self.player.rect.x
        if self.state == self.STATE_ATTACKING:
            self._continue_attack()


    def _continue_attack(self) -> None:
        """ Gerencia a animação de ataque. """
        if self.duration_counter > 0:
            self._attack_animation()
            self._perform_attack()
            self.duration_counter -= 1
        else:
            self._reset_to_idle()


    def _attack_animation(self) -> None:
        """ Avança os frames da animação de ataque. """
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.player.cannon_frames)
            self._update_attack_hitbox()
            print(f'frame: {self.current_frame_index}')
        self._update_player_image()


    def _update_player_image(self) -> None:
        """ Atualiza a imagem do player com base no frame de ataque atual. """
        self.player.image = self.player.cannon_frames[self.current_frame_index]
        self.player.rect = self.player.image.get_rect()
        self.player.rect.centerx = self.player_x
        self.player.rect.bottom = self.initial_rect.bottom + 6


    def _update_attack_hitbox(self) -> None:
        """ Atualiza a hitbox de ataque com base no frame atual. """
        if self.current_frame_index < 3:
            self.attack_hitbox.size = (50, 50)
        elif 3 <= self.current_frame_index < 6:
            self.attack_hitbox.size = (370, 250)
        else:
            self.attack_hitbox.size = (50, 50)
            
        self.attack_hitbox.centerx = self.player.rect.centerx
        self.attack_hitbox.bottom = self.player.rect.bottom


    def _reset_to_idle(self) -> None:
        """ Reseta o estado de ataque e notifica os listeners. """
        self.state = self.STATE_IDLE
        self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
        self.animation_counter = 0
        self.current_frame_index = 0
        self.duration_counter = 0
        self.hit_targets.clear()
        self._reset_attack_hitbox()


    def _perform_attack(self) -> None:
        """ Verifica a colisão com alvos e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_mob_sprites'})
        for target in target_sprites:
            if self.attack_hitbox.colliderect(target.rect) and target not in self.hit_targets:
                self._inflict_damage(target)
                self.hit_targets.add(target)


    def _inflict_damage(self, target) -> None:
        """ Inflige dano ao alvo e lida com os eventos relativos. """
        damage = self.player.attack_damage
        target.receive_damage(damage)
        self._knockback_target(target)
        self._check_target_life(target)


    def _knockback_target(self, target) -> None:
        """ Aplica efeito de recuo no alvo com base na posição do player. """
        if target.rect.centerx <= self.player.rect.centerx:
            target.rect.centerx -= 90
        else:
            target.rect.centerx += 90


    def _check_target_life(self, target) -> None:
        """ Verifica se a vida do alvo chegou a zero e lida de acordo. """
        if target.life <= 0:
            target.defeat()
            target.kill()


    def _reset_attack_hitbox(self) -> None:
        """ Reseta a hitbox do ataque com base na posição do player. """
        self.attack_hitbox = pygame.Rect(self.player.rect.centerx - 25, self.player.rect.bottom - 50, 50, 50)