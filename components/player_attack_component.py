import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):
    """ Classe para gerenciar o componente de ataque do player. """

    ATTACK_DURATION = 44
    ANIMATION_SPEED = 0.20
    CANNON_ATTACK_DURATION = 95
    CANNON_ANIMATION_SPEED = 0.36
    STATE_IDLE = 'idle'
    STATE_ATTACKING = 'attacking'
    KNOCKBACK_DISTANCE = 90

    def __init__(self, player, sound, event_manager) -> None:
        super().__init__()
        self.player = player
        self.sound = sound
        self.event_manager = event_manager
        self.state = self.STATE_IDLE
        self.attack_duration = self.ATTACK_DURATION
        self.animation_speed = self.ANIMATION_SPEED
        self.cannon_attack_duration = self.CANNON_ATTACK_DURATION
        self.cannon_animation_speed = self.CANNON_ANIMATION_SPEED
        self.frame_counter = 0
        self.current_frame_index = 0
        self.duration_timer = 0
        self.attack_type = None
        self.initial_rect = player.rect.copy()
        self.attack_hitbox = pygame.Rect(self.player.rect.centerx, self.player.rect.centery, 50, 50)
        self.hit_targets = set()


    def attack(self, attack_type: int) -> None:
        """ Inicia o ataque se estiver inativo e notifica os listeners. """
        if self.state == self.STATE_IDLE:
            self.attack_type = attack_type
            self.state = self.STATE_ATTACKING
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self._start_attack()


    def update(self) -> None:
        """ Atualiza a posição do player e o estado de ataque. """
        if self.state == self.STATE_ATTACKING:
            self._continue_attack()


    def _start_attack(self) -> None:
        if self.attack_type == 1:
            self.animation_speed = self.ANIMATION_SPEED
            self.duration_timer = self.attack_duration
            self.sound.play()
        elif self.attack_type == 2:
            self.animation_speed = self.CANNON_ANIMATION_SPEED
            self.duration_timer = self.cannon_attack_duration
            # sound cannon


    def _continue_attack(self) -> None:
        """ Gerencia a animação de ataque. """
        if self.duration_timer > 0:
            self._attack_animation()
            self._perform_attack()
            self.duration_timer -= 1
        else:
            self._reset_to_idle()


    def _attack_animation(self) -> None:
        """ Avança os frames da animação de ataque. """
        if self.frame_counter == 0 and self.current_frame_index == 0:
            # Garantir a atualização inicial
            self._update_player_image()
            self._update_attack_hitbox()

        self.frame_counter += self.animation_speed
        if self.frame_counter >= 1:
            self.frame_counter = 0
            if self.attack_type == 1:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.player.attack_frames)
            elif self.attack_type == 2:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.player.cannon_frames)
            self._update_attack_hitbox()
        self._update_player_image()


    def _update_player_image(self) -> None:
        """ Atualiza a imagem do player com base no frame de ataque atual. """
        if self.attack_type == 1:
            self.player.image = self.player.attack_frames[self.current_frame_index]
        elif self.attack_type == 2:
            self.player.image = self.player.cannon_frames[self.current_frame_index]
        self.player.rect = self.player.image.get_rect()
        self.player.rect.centerx = self.initial_rect.centerx
        self.player.rect.bottom = self.initial_rect.bottom + 6


    def _update_attack_hitbox(self) -> None:
        """ Atualiza a hitbox de ataque com base no frame atual. """
        if self.attack_type == 1:
            if self.current_frame_index < 3:
                self.attack_hitbox.size = (50, 50)
            elif 3 <= self.current_frame_index < 6:
                self.attack_hitbox.size = (370, 250)
            else:
                self.attack_hitbox.size = (50, 50)
        elif self.attack_type == 2:
            if self.current_frame_index < 4:
                self.attack_hitbox.size = (100, 150)
            elif self.current_frame_index < 16:
                self.attack_hitbox.size = (310, 150)
            elif self.current_frame_index < 18:
                self.attack_hitbox.size = (450, 150)
            elif self.current_frame_index < 20:
                self.attack_hitbox.size = (520, 150)
            elif self.current_frame_index < 21:
                self.attack_hitbox.size = (570, 150)
            elif self.current_frame_index < 22:
                self.attack_hitbox.size = (590, 150)
            elif self.current_frame_index < 23:
                self.attack_hitbox.size = (650, 150)
            elif self.current_frame_index < 24:
                self.attack_hitbox.size = (670, 150)
            elif self.current_frame_index < 25:
                self.attack_hitbox.size = (690, 150)
            
        self.attack_hitbox.centerx = self.player.rect.centerx
        self.attack_hitbox.bottom = self.player.rect.bottom


    def _reset_to_idle(self) -> None:
        """ Reseta o estado de ataque e notifica os listeners. """
        self.state = self.STATE_IDLE
        self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
        self.frame_counter = 0
        self.current_frame_index = 0
        self.duration_timer = 0
        self.hit_targets.clear()
        self._reset_attack_hitbox()


    def _perform_attack(self) -> None:
        """ Verifica a colisão com alvos e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_mob_sprites'})
        for target in target_sprites:
            if self.attack_type == 1:
                if self.attack_hitbox.colliderect(target.rect) and target not in self.hit_targets:
                    self._inflict_damage(target)
                    self.hit_targets.add(target)
            elif self.attack_type == 2:
                if self.attack_hitbox.colliderect(target.rect):
                    self._inflict_damage(target)


    def _inflict_damage(self, target) -> None:
        """ Inflige dano ao alvo e lida com os eventos relativos. """
        damage = self.player.attack_damage
        target.receive_damage(damage)
        self._knockback_target(target)
        self._check_target_life(target)


    def _knockback_target(self, target) -> None:
        """ Aplica efeito de recuo no alvo com base na posição do player. """
        if target.rect.centerx <= self.player.rect.centerx:
            target.rect.centerx -= self.KNOCKBACK_DISTANCE
        else:
            target.rect.centerx += self.KNOCKBACK_DISTANCE


    def _check_target_life(self, target) -> None:
        """ Verifica se a vida do alvo chegou a zero e lida de acordo. """
        if target.life <= 0:
            target.defeat()
            target.kill()


    def _reset_attack_hitbox(self) -> None:
        """ Reseta a hitbox do ataque com base na posição do player. """
        self.attack_hitbox = pygame.Rect(self.player.rect.centerx - 25, self.player.rect.bottom - 50, 50, 50)