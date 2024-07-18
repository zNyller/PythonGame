import pygame
from components.attack_component import AttackComponent
from managers.event_manager import EventManager
from entities.player import Player
from entities.mob import Mob

class BasicAttackComponent(AttackComponent):
    """Componente de ataque para as entidades do jogo.

    Este componente gerencia o estado de ataque da entidade, incluindo a duração,
    a aplicação de dano aos alvos atingidos e a reprodução de sons de ataque.
    """

    def __init__(
            self, 
            entity: Player | Mob, 
            damage: int, 
            attack_duration: int, 
            attack_range: int, 
            attack_sound: pygame.mixer.Sound, 
            event_manager: EventManager
        ) -> None:
        """Inicializa os atributos para genrenciar os ataques."""
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
        self.cooldown_duration = 40

    def attack(self) -> None:
        """Inicia a ação e duração do ataque se não estiver em cooldown."""
        if self.state == self.IDLE_STATE and self.attack_cooldown == 0:
            self.state = self.ATTACK_STATE
            self.attack_duration = self.initial_attack_duration
            self.attack_cooldown = self.cooldown_duration
            self._set_attack_position()

    def update(self) -> None:
        """Atualiza o estado de ataque."""
        if self.state == self.ATTACK_STATE:
            if self.attack_duration > 0:
                self._perform_attack()
                self._update_attack_movement()
                self.attack_duration -= 1
            else:
                self._reset_attack()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def _set_attack_position(self) -> None:
        """Define a posição inicial e final para o movimento de ataque."""
        self.attack_start_position = self.entity.rect.centerx
        direction_factor = 1 if self.entity.direction == 1 else -1
        self.attack_end_position = (self.entity.rect.centerx + direction_factor * self.attack_range)

    def _perform_attack(self) -> None:
        """Verifica colisão com o jogador e inflige dano."""
        target_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        for target in target_sprites:
            if self.entity.rect.colliderect(target.rect) and not self.hit_target:
                self.hit_target = True
                self._set_attacking_image()
                self.inflict_damage(target, self.attack_damage)
                self._move_through_target(target)

    def _update_attack_movement(self) -> None:
        """Incrementa o progresso do ataque e move a entidade gradualmente. 
        
        Este método atualiza a posição da entidade com base no progresso atual do ataque,
        calculando a nova posição horizontal (x). 
        O ataque é considerado concluído quando o progresso atinge ou ultrapassa 1. 

        """
        if self.attack_start_position is not None and self.attack_end_position is not None:
            self.attack_progress += 1 / self.initial_attack_duration
            new_x = int(self.attack_start_position + (self.attack_end_position - self.attack_start_position) * self.attack_progress)
            self.entity.rect.centerx = new_x
            self._check_attack_progress()

    def _check_attack_progress(self) -> None:
        """Marca hit_target como True ou False baseado no progresso do ataque. 
        
        hit_target = True evita danos consecutivos em um mesmo ataque, enquanto
        hit_target = False permite aplicação de dano novamente, após a conclusão do ataque.
        """
        self.hit_target = self.attack_progress <= 1

    def _set_attacking_image(self) -> None:
        """Aplica a imagem de ataque com base na direção da entidade."""
        if hasattr(self.entity, 'attack_image'):
            self.entity.image = (self.entity.attack_image if self.entity.direction == 1 
                                else pygame.transform.flip(self.entity.attack_image, True, False))
        elif hasattr(self.entity, 'attack_frames'):
            self.entity.image = (self.entity.attack_frames[0] if self.entity.direction == 1 
                                else pygame.transform.flip(self.entity.attack_frames[0], True, False))
        else:
            raise ValueError("Imagem de ataque não reconhecida!")

    def _move_through_target(self, target: Player | Mob) -> None:
        """Move a entidade para atravessar o alvo durante o ataque."""
        move_distance = self.attack_range
        self.entity.rect.centerx += move_distance if target.rect.centerx >= self.entity.rect.centerx else -move_distance

    def _reset_attack(self) -> None:
        """Retorna a imagem da entidade à sua imagem padrão."""
        if hasattr(self.entity, 'default_image'):
            self.entity.image = (self.entity.default_image if self.entity.direction == 1
                                else pygame.transform.flip(self.entity.default_image, True, False))
        elif hasattr(self.entity, 'default_frames'):
            self.entity.image = (self.entity.default_frames[0] if self.entity.direction == 1 
                                else pygame.transform.flip(self.entity.default_frames[0], True, False))
        else:
            raise ValueError("Imagem padrão não reconhecida!")
        self.state = self.IDLE_STATE
        self.attack_progress = 0