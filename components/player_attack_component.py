import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):
    """ Classe para gerenciar o componente de ataque do player. """

    ATTACK_DURATION = 1.1
    ANIMATION_SPEED = 9
    CANNON_ATTACK_DURATION = 2.5
    CANNON_ANIMATION_SPEED = 15.5
    STATE_IDLE = 'idle'
    STATE_ATTACKING = 'attacking'
    KNOCKBACK_DISTANCE = 90

    def __init__(self, player, sounds, event_manager) -> None:
        super().__init__()
        self.player = player
        self.sounds = sounds
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
        self.attack_hitbox = pygame.Rect(0, 0, 50, 50)
        self.hit_targets = set()
        self.first_attack = True


    def attack(self, attack_type: int) -> None:
        """ Inicia o ataque se estiver inativo e notifica os listeners. """
        if self.state == self.STATE_IDLE:
            self.attack_type = attack_type
            self.state = self.STATE_ATTACKING
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self._start_attack()


    def update(self, delta_time) -> None:
        """ Atualiza o estado de ataque. """
        if self.state == self.STATE_ATTACKING:
            self._continue_attack(delta_time)
            print(f'delta_time: {delta_time}')


    def _start_attack(self) -> None:
        if self.attack_type == 1:
            self.animation_speed = self.ANIMATION_SPEED
            self.duration_timer = self.attack_duration
            if self.first_attack:
                #self.sounds.get('attack_sound').play()
                self.first_attack = False
            else:
                #self.sounds.get('attack_sound_2').play()
                self.first_attack = True
        elif self.attack_type == 2:
            self.animation_speed = self.CANNON_ANIMATION_SPEED
            self.duration_timer = self.cannon_attack_duration
            #self.sounds.get('cannon_sound').play()


    def _continue_attack(self, delta_time) -> None:
        """ Verifica a duração da animação de ataque e lida de acordo. """
        if self.duration_timer > 0:
            self._attack_animation(delta_time)
            self._perform_attack()
            self.duration_timer -= delta_time
        else:
            self._reset_to_idle()


    def _attack_animation(self, delta_time) -> None:
        """ Avança os frames da animação de ataque. """
        self._update_attack_hitbox()
        self.frame_counter += self.animation_speed * delta_time
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self._increment_frame_index()
            self._update_attack_hitbox()
        self._update_player_image()


    def _increment_frame_index(self) -> None:
        """ Incrementa o índice de frame de acordo com o tipo de ataque. """
        frames = self.player.attack_frames if self.attack_type == 1 else self.player.cannon_frames
        self.current_frame_index += 1
        if self.current_frame_index >= len(frames):
            self.current_frame_index = 0
        print(f'frame: {self.current_frame_index}')


    def _update_player_image(self) -> None:
        """ Atualiza a imagem do player com base no frame de ataque atual. """
        self.player.image = self._get_current_frame()
        if self.player.movement_component.facing_right:
            self.player.image = pygame.transform.flip(self.player.image, True, False)
        self.player.rect = self.player.image.get_rect(centerx=self.player.rect.centerx, bottom = self.initial_rect.bottom + 6)


    def _get_current_frame(self) -> pygame.Surface:
        """ Retorna o frame atual baseado no tipo de ataque. """
        return self.player.attack_frames[self.current_frame_index] if self.attack_type == 1 else self.player.cannon_frames[self.current_frame_index]


    def _update_attack_hitbox(self) -> None:
        """ Atualiza a hitbox de ataque com base no frame atual e na direção do jogador. """
        attack_width, attack_height = self._get_attack_hitbox_size()
        offset_x = 20 if self.player.movement_component.facing_right else -20

        self.attack_hitbox.size = (attack_width, attack_height)
        self.attack_hitbox.centerx = self.player.rect.centerx + offset_x


    def _get_attack_hitbox_size(self) -> tuple:
        """ Retorna o tamanho da hitbox de acordo com o tipo de ataque atual. """
        return self._get_sword_hitbox_size() if self.attack_type == 1 else self._get_cannon_hitbox_size()
            

    def _get_sword_hitbox_size(self) -> tuple[int, int]:
        """ Retorna o tamanho da hitbox baseado no frame atual. """
        if 3 <= self.current_frame_index < 6:
            return (310, 250)
        else:
            return (100, 150)
        

    def _get_cannon_hitbox_size(self) -> tuple[int, int]:
        """ Retorna o tamanho da hitbox baseado no frame atual. """
        if self.current_frame_index < 4:
            return (100, 150)
        elif self.current_frame_index < 16:
            return (250, 150)
        elif self.current_frame_index < 18:
            return (450, 150)
        elif self.current_frame_index < 20:
            return (520, 150)
        elif self.current_frame_index < 21:
            return (570, 150)
        elif self.current_frame_index < 22:
            return (590, 150)
        elif self.current_frame_index < 23:
            return (650, 150)
        elif self.current_frame_index < 24:
            return (670, 150)
        elif self.current_frame_index < 25:
            return (690, 150)
        else:
            return (100, 150)
        

    def _reset_to_idle(self) -> None:
        """ Reseta o estado de ataque e notifica os listeners. """
        self.state = self.STATE_IDLE
        self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
        self.frame_counter = 0
        self.current_frame_index = 0
        self.duration_timer = 0
        self.hit_targets.clear()
        self._reset_attack_hitbox()


    def _reset_attack_hitbox(self) -> None:
        """ Reseta a hitbox do ataque com base na posição do player. """
        self.attack_hitbox = pygame.Rect(self.player.rect.centerx - 25, self.player.rect.bottom - 50, 50, 50)


    def _perform_attack(self) -> None:
        """ Verifica a colisão com alvos e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_mob_sprites'})
        for target in target_sprites:
            if self.attack_type == 1 and self._hit_target(target):
                self._inflict_damage(target, self.player.attack_damage)
                self.hit_targets.add(target)
            elif self.attack_type == 2 and self._hit_target(target):
                self._inflict_damage(target, self.player.cannon_damage)


    def _hit_target(self, target) -> bool:
        """ Verifica se o alvo foi atingido pelo ataque e retorna true ou false. """
        return self.attack_hitbox.colliderect(target.rect) and target not in self.hit_targets


    def _inflict_damage(self, target, damage: int) -> None:
        """ Inflige dano ao alvo e lida com os eventos relativos. """
        target.receive_damage(damage)
        self._knockback_target(target)
        self._check_target_life(target)


    def _knockback_target(self, target) -> None:
        """ Aplica efeito de recuo no alvo com base na posição do player. """
        if self.player.rect.centerx <= target.rect.centerx:
            target.rect.centerx += self.KNOCKBACK_DISTANCE  # Move o alvo para a direita
        else:
            target.rect.centerx -= self.KNOCKBACK_DISTANCE  # Move o alvo para a esquerda


    def _check_target_life(self, target) -> None:
        """ Verifica se a vida do alvo chegou a zero e lida de acordo. """
        if target.life <= 0:
            target.defeat()
            target.kill()