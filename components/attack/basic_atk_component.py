import pygame
from typing import TYPE_CHECKING, Union
from .atk_component_interface import AttackComponent

if TYPE_CHECKING:
    from managers.event_manager import EventManager
    from entities.player import Player
    from entities.mob import Mob

class BasicAttackComponent(AttackComponent):
    """Componente de ataque para as entidades do jogo.

    Este componente gerencia o estado de ataque da entidade, incluindo a duração,
    a aplicação de dano aos alvos atingidos e a reprodução de sons de ataque.
    """

    STATIC_ATTACK = 'static'
    ANIMATED_ATTACK = 'animated'

    def __init__(
            self, 
            entity: Union['Player', 'Mob'], 
            damage: int, 
            attack_duration: int, 
            attack_range: int, 
            attack_sound: pygame.mixer.Sound, 
            event_manager: 'EventManager'
        ) -> None:
        """Inicializa os atributos para genrenciar os ataques."""
        super().__init__(entity)
        self._entity = entity
        self._attack_damage = damage
        self._initial_attack_duration = self.attack_duration = attack_duration
        self._attack_range = attack_range
        self._attack_sound = attack_sound
        self._event_manager = event_manager
        self._attack_feature = (
            self.STATIC_ATTACK if entity.type == 'Soul' else self.ANIMATED_ATTACK
        )
        self._hit_target = False
        self._attack_start_position = self._attack_end_position = None
        self._attack_progress = 0
        self._attack_cooldown = 0
        self._cooldown_duration = 40

    def attack(self) -> None:
        """Inicia a ação e duração do ataque se não estiver em cooldown."""
        if self.state == self.IDLE_STATE and self._attack_cooldown == 0:
            self.state = self.ATTACK_STATE
            self.attack_duration = self._initial_attack_duration
            self._attack_cooldown = self._cooldown_duration
            self._set_attack_position()

    def update(self) -> None:
        """Atualiza o estado de ataque."""
        if self.state == self.ATTACK_STATE:
            if self.attack_duration > 0:
                self._perform_attack()
                if self._attack_feature == self.STATIC_ATTACK:
                    self._update_attack_movement()
                self.attack_duration -= 1
            else:
                self._reset_attack()
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1

    def _set_attack_position(self) -> None:
        """Define a posição inicial e final para o movimento de ataque."""
        self._attack_start_position = self._entity.rect.centerx
        direction_factor = 1 if self._entity.direction == 1 else -1
        self._attack_end_position = (self._entity.rect.centerx + direction_factor * self._attack_range)

    def _perform_attack(self) -> None:
        """Verifica colisão com o jogador e inflige dano."""
        target_sprites = self._event_manager.notify({'type': 'get_player_sprites'})
        for target in target_sprites:
            if self._entity.rect.colliderect(target.rect) and not self._hit_target:
                self._hit_target = True
                self._set_attacking_image()
                self.inflict_damage(target, self._attack_damage)
                if self._attack_feature == self.STATIC_ATTACK:
                    self._move_through_target(target)
                elif self._attack_feature == self.ANIMATED_ATTACK:
                    self.knockback_entity(target)

    def _update_attack_movement(self) -> None:
        """Incrementa o progresso do ataque e move a entidade gradualmente. 
        
        Este método atualiza a posição da entidade com base no progresso atual do ataque,
        calculando a nova posição horizontal (x). 
        O ataque é considerado concluído quando o progresso atinge ou ultrapassa 1. 
        """
        if self._attack_start_position is not None and self._attack_end_position is not None:
            self._attack_progress += 1 / self._initial_attack_duration
            new_x = int(self._attack_start_position + (self._attack_end_position - self._attack_start_position) * self._attack_progress)
            self._entity.rect.centerx = new_x
            self._check__attack_progress()

    def _check__attack_progress(self) -> None:
        """Marca _hit_target como True ou False baseado no progresso do ataque. 
        
        _hit_target = True evita danos consecutivos em um mesmo ataque, enquanto
        _hit_target = False permite aplicação de dano novamente, após a conclusão do ataque.
        """
        self._hit_target = self._attack_progress <= 1

    def _set_attacking_image(self) -> None:
        """Aplica a imagem de ataque com base na direção da entidade."""
        if hasattr(self._entity, 'attack_image'):
            self._entity.image = (self._entity.attack_image if self._entity.direction == 1 
                                else pygame.transform.flip(self._entity.attack_image, True, False))
        elif hasattr(self._entity, 'attack_frames'):
            self._entity.image = (self._entity.attack_frames[0] if self._entity.direction == 1 
                                else pygame.transform.flip(self._entity.attack_frames[0], True, False))
        else:
            raise ValueError(f"Imagem de ataque não encontrada para {self._entity}!")

    def _move_through_target(self, target: Union['Player', 'Mob']) -> None:
        """Move a entidade para atravessar o alvo durante o ataque."""
        move_distance = self._attack_range
        self._entity.rect.centerx += (
            move_distance if target.rect.centerx >= self._entity.rect.centerx 
            else -move_distance
        )

    def _reset_attack(self) -> None:
        """Retorna a imagem da entidade à sua imagem padrão."""
        if hasattr(self._entity, 'default_image'):
            self._entity.image = (
                self._entity.default_image if self._entity.direction == 1
                else pygame.transform.flip(self._entity.default_image, True, False)
            )
        elif hasattr(self._entity, 'default_frames'):
            self._entity.image = (
                self._entity.default_frames[0] if self._entity.direction == 1 
                else pygame.transform.flip(self._entity.default_frames[0], True, False)
            )
        else:
            raise ValueError("Imagem padrão não reconhecida!")
        self.state = self.IDLE_STATE
        self._attack_progress = 0
        self._hit_target = False