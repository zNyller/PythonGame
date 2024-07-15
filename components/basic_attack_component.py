import pygame
from components.attack_component import AttackComponent

class BasicAttackComponent(AttackComponent):
    """
    Componente de ataque para as entidade do jogo.

    Este componente gerencia o estado de ataque da entidade, incluindo a duração,
    a aplicação de dano aos alvos atingidos e a reprodução de sons de ataque.
    """

    def __init__(self, entity, damage: int, attack_duration: int, attack_range: int, attack_sound, event_manager):
        super().__init__(entity)
        self.entity = entity
        self.attack_damage = damage
        self.initial_attack_duration = self.attack_duration = attack_duration
        self.attack_range = attack_range
        self.attack_sound = attack_sound
        self.event_manager = event_manager
        self.hit_target = False
        self.attack_start_position = self.attack_end_position = None
        self.attack_progress = 0
        self.attack_cooldown = 0
        self.cooldown_duration = 30


    def attack(self):
        """ Inicia a ação e duração do ataque se não estiver em cooldown. """
        if self.state == self.IDLE_STATE and self.attack_cooldown == 0:
            self.state = self.ATTACK_STATE
            self.attack_duration = self.initial_attack_duration
            self.attack_cooldown = self.cooldown_duration
            self._set_attack_position()


    def update(self):
        """ Atualiza o estado de ataque. """
        if self.state == self.ATTACK_STATE:
            if self.attack_duration > 0:
                self._perform_attack()
                self._update_attack_movement()
                self.attack_duration -= 1
            else:
                self._reset_attack()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


    def _set_attack_position(self):
        """ Define a posição inicial e final para o movimento de ataque. """
        self.attack_start_position = self.entity.rect.centerx
        direction_factor = 1 if self.entity.direction == 1 else -1
        self.attack_end_position = (self.entity.rect.centerx + self.attack_range 
                                    if direction_factor == 1 
                                    else self.entity.rect.centerx - self.attack_range)
        self.attack_progress = 0


    def _perform_attack(self):
        """ Verifica colisão com o jogador e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        for target in target_sprites:
            if self.entity.rect.colliderect(target.rect) and not self.hit_target:
                self.hit_target = True
                self._set_attacking_image()
                self.inflict_damage(target, self.attack_damage)
                self._move_trough_target(target)


    def _update_attack_movement(self):
        """ Move a entidade gradualmente durante o ataque. """
        if self.attack_start_position is not None and self.attack_end_position is not None:
            # Incrementar o progresso do ataque
            self.attack_progress += 1 / self.initial_attack_duration
            new_x = int(self.attack_start_position + (self.attack_end_position - self.attack_start_position) * self.attack_progress)
            self.entity.rect.centerx = new_x
            self._check_attack_progress()
            

    def _check_attack_progress(self):
        """ Verifica o progresso do ataque e marca hit_target como False para permitir um novo ataque. """
        self.hit_target = False if self.attack_progress >= 1 else True


    def _set_attacking_image(self):
        """ Aplica a imagem de ataque com base na direção da entidade. """
        self.entity.image = (self.entity.attacking_image if self.entity.direction == 1 
                             else pygame.transform.flip(self.entity.attacking_image, True, False))


    def _move_trough_target(self, target):
        """ Move a entidade para atravessar o alvo durante o ataque. """
        move_distance = self.attack_range
        self.entity.rect.centerx += move_distance if target.rect.centerx >= self.entity.rect.centerx else -move_distance


    def _reset_attack(self):
        """ Retorna a imagem da entidade à sua imagem padrão. """
        self.entity.image = self.entity.default_frames
        self.state = self.IDLE_STATE