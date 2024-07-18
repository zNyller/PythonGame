from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY
from entities.mob import Mob
from components.basic_attack_component import BasicAttackComponent
from managers.event_manager import EventManager

class MobMovementComponent:
    """Gerencia a movimentação do mob verificando colisões e limites da tela."""

    def __init__(
            self, 
            mob: Mob, 
            attack_component: BasicAttackComponent, 
            event_manager: EventManager
        ) -> None:
        """Inicializa os atributos necessários para gerenciar os movimentos."""
        self.mobs = [mob]
        self.attack_component = attack_component
        self.event_manager = event_manager

    def handle_collision(self, delta_time: float) -> None:
        """Verifica se houve colisão com o player e lida de acordo."""
        for mob in self.mobs:
            self.move(mob, delta_time) if not self.has_collided(mob) else self.attack_component.attack()

    def has_collided(self, mob: Mob) -> bool:
        """Verifica colisão com o jogador considerando uma distância mínima."""
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for target in player_sprites:
                distance_threshold = 150  # Distância mínima para considerar colisão
                if abs(mob.rect.centerx - target.rect.centerx) <= distance_threshold:
                    return True
        return False

    def move(self, mob: Mob, delta_time: float) -> None:
        """Move o mob e limita o movimento dentro das bordas."""
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for player in player_sprites:
                if mob.rect.centerx <= player.rect.centerx:
                    mob.direction = 1
                    mob.rect.x += mob.speed * delta_time
                elif mob.rect.centerx >= player.rect.centerx:
                    mob.direction = -1
                    mob.rect.x -= mob.speed * delta_time
                self._limit_movements(mob)

    def _limit_movements(self, mob: Mob) -> None:
        """Limita os movimentos do mob dentro da janela do jogo."""
        if mob.rect.left < LEFT_BOUNDARY or mob.rect.right > RIGHT_BOUNDARY:
            mob.rect.center = mob.initial_position