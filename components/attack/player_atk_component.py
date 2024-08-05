from typing import TYPE_CHECKING, Dict, Tuple
from .atk_component_interface import AttackComponent
from .atk_animation_component import AttackAnimationComponent
from .atk_hitbox_component import AttackHitboxComponent

if TYPE_CHECKING:
    from pygame.mixer import Sounds
    from entities.player import Player
    from managers.event_manager import EventManager

class PlayerAttackComponent(AttackComponent):
    """Gerencia o componente de ataque do player."""

    def __init__(
            self, 
            player: 'Player', 
            sounds: Dict[str, 'Sounds'], 
            event_manager: 'EventManager'
        ) -> None:
        """Inicializa o componente de ataque do Player."""
        super().__init__(player)
        self._player = player
        self._sounds = sounds
        self._event_manager = event_manager
        self._attack_animation = AttackAnimationComponent(player)
        self._attack_hitbox = AttackHitboxComponent(player)
        self._hit_targets = set()
        self._first_attack = True

    def attack(self, attack_type: int) -> None:
        """Inicia o ataque se estiver inativo e notifica os listeners."""
        if self.state == self.IDLE_STATE:
            self.state = self.ATTACK_STATE
            self._attack_animation.start_animation(attack_type)
            self._event_manager.notify({'type': 'player_attack', 'state': 'start'})

    def update(self, delta_time: float) -> None:
        """Atualiza o estado de ataque."""
        if self.state == self.ATTACK_STATE:
            self._attack_animation.update(delta_time)
            self._attack_hitbox.update_hitbox(
                self._attack_animation.attack_type, 
                self._attack_animation.current_frame_index
            )
            self._perform_attack()
            if self._attack_animation.duration_timer <= 0:
                self._reset_attack()

    def _perform_attack(self) -> None:
        """Verifica a colisão com alvos e inflige dano."""
        target_sprites = self._event_manager.notify({'type': 'get_mob_sprites'})
        attack_type = self._attack_animation.attack_type
        damage, add_to__hit_targets = self._get_attack_details(attack_type)
        
        for target in target_sprites:
            if self._attack_hitbox.hit_target(target) and target not in self._hit_targets:
                self.inflict_damage(target, damage)
                self.knockback_target(target)
                if add_to__hit_targets:
                    self._hit_targets.add(target)

    def _get_attack_details(self, attack_type: int) -> Tuple[int, bool]:
        """Configura os detalhes do ataque com base no tipo."""
        if attack_type == 1:
            return self._player.attack_damage, True
        elif attack_type == 2:
            return self._player.cannon_damage, False
        else:
            raise ValueError(f"Tipo de ataque desconhecido: {attack_type}")

    def _reset_attack(self) -> None:
        """Reseta o estado de ataque e notifica os listeners."""
        self.state = self.IDLE_STATE
        self._attack_animation.reset()
        self._hit_targets.clear()
        self._event_manager.notify({'type': 'player_attack', 'state': 'end'})