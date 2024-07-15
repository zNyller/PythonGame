from config.constants import LEFT_BOUNDARY, RIGHT_BOUNDARY

class MobMovementComponent:
    """ Gerencia a movimentação do mob verificando colisões e limites da tela. """

    def __init__(self, mob, attack_component, event_manager) -> None:
        """ Inicializa os atributos necessários para gerenciar os movimentos. """
        self.mob = mob
        self.attack_component = attack_component
        self.event_manager = event_manager


    def handle_collision(self, delta_time) -> None:
        """ Verifica se houve colisão com o player e lida de acordo. """
        self.move(delta_time) if not self.has_collided() else self.attack_component.attack()


    def has_collided(self) -> bool:
        """ Verifica colisão com o jogador considerando uma distância mínima. """
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for target in player_sprites:
                distance_threshold = 150  # Distância mínima para considerar colisão
                if abs(self.mob.rect.centerx - target.rect.centerx) <= distance_threshold:
                    return True
        return False


    def move(self, delta_time) -> None:
        """ Move o mob e limita o movimento dentro das bordas. """
        player_sprites = self.event_manager.notify({'type': 'get_player_sprites'})
        if player_sprites:
            for player in player_sprites:
                if self.mob.rect.centerx <= player.rect.centerx:
                    self.mob.direction = 1
                    self.mob.rect.x += self.mob.speed * delta_time
                else:
                    self.mob.direction = -1
                    self.mob.rect.x -= self.mob.speed * delta_time
                self._limit_movements()


    def _limit_movements(self) -> None:
        """ Limita os movimentos do mob dentro da janela do jogo. """
        if self.mob.rect.left < LEFT_BOUNDARY or self.mob.rect.right > RIGHT_BOUNDARY:
            self.mob.rect.center = self.INITIAL_POSITION