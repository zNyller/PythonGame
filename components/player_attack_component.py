from components.attack_component import AttackComponent
from components.attack_animation import AttackAnimation
from components.attack_hitbox import AttackHitbox

class PlayerAttackComponent(AttackComponent):
    """ Classe para gerenciar o componente de ataque do player. """

    def __init__(self, player, sounds, event_manager) -> None:
        super().__init__(player, event_manager)
        self.player = player
        self.sounds = sounds
        self.attack_animation = AttackAnimation(player)
        self.attack_hitbox = AttackHitbox(player)
        self.hit_targets = set()
        self.first_attack = True


    def attack(self, attack_type: int) -> None:
        """ Inicia o ataque se estiver inativo e notifica os listeners. """
        if self.state == self.STATE_IDLE:
            self.state = self.STATE_ATTACKING
            self.attack_animation.start_animation(attack_type)
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})


    def update(self, delta_time) -> None:
        """ Atualiza o estado de ataque. """
        if self.state == self.STATE_ATTACKING:
            self.attack_animation.update_animation(delta_time)
            self.attack_hitbox.update_hitbox(self.attack_animation.attack_type, 
                                             self.attack_animation.current_frame_index)
            self._perform_attack()
            if self.attack_animation.duration_timer <= 0:
                self._reset_attack()


    def _perform_attack(self) -> None:
        """ Verifica a colisão com alvos e inflige dano. """
        target_sprites = self.event_manager.notify({'type': 'get_mob_sprites'})
        attack_type = self.attack_animation.attack_type
        damage, add_to_hit_targets = self._get_attack_details(attack_type)
        
        for target in target_sprites:
            if self.attack_hitbox.hit_target(target) and target not in self.hit_targets:
                self.inflict_damage(target, damage)
                self.knockback_target(target)
                if add_to_hit_targets:
                    self.hit_targets.add(target)


    def _get_attack_details(self, attack_type):
        """ Configura os detalhes do ataque com base no tipo. """
        if attack_type == 1:
            return self.player.attack_damage, True
        elif attack_type == 2:
            return self.player.cannon_damage, False
        else:
            raise ValueError(f"Tipo de ataque desconhecido: {attack_type}")


    def _inflict_damage(self, target, damage: int) -> None:
        """ Inflige dano ao alvo e lida com os eventos relativos. """
        target.receive_damage(damage)
        self.check_target_life(target)


    def _reset_attack(self) -> None:
        """ Reseta o estado de ataque e notifica os listeners. """
        self.state = self.STATE_IDLE
        self.attack_animation.reset()
        self.hit_targets.clear()
        self.event_manager.notify({'type': 'player_attack', 'state': 'end'})