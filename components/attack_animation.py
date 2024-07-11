import pygame

class AttackAnimation:

    ATTACK_DURATION = 1.1
    ANIMATION_SPEED = 9
    CANNON_ATTACK_DURATION = 2.5
    CANNON_ANIMATION_SPEED = 15.5


    def __init__(self, player) -> None:
        self.player = player
        self._attack_type = None
        self.frame_counter = self.current_frame_index = self.duration_timer = 0
        self.initial_rect = player.rect.copy()


    def start_animation(self, attack_type):
        """ Inicia a animação de acordo com o tipo de ataque. """
        self._attack_type = attack_type
        if attack_type == 1:
            self.animation_speed = self.ANIMATION_SPEED
            self.duration_timer = self.ATTACK_DURATION
        elif attack_type == 2:
            self.animation_speed = self.CANNON_ANIMATION_SPEED
            self.duration_timer = self.CANNON_ATTACK_DURATION


    def update_animation(self, delta_time) -> None:
        """ Avança os frames da animação de ataque. """
        if self.duration_timer > 0:
            print(f'frame: {self.current_frame_index}')
            self.frame_counter += self.animation_speed * delta_time
            if self.frame_counter >= 1:
                self.frame_counter = 0
                self._increment_frame_index()
            self._update_player_image()
            self.duration_timer -= delta_time
        else:
            self.reset()  # Ensure the animation resets when the duration is over


    def _increment_frame_index(self) -> None:
        """ Incrementa o índice de frame de acordo com o tipo de ataque. """
        frames = self.player.attack_frames if self.attack_type == 1 else self.player.cannon_frames
        self.current_frame_index += 1
        if self.current_frame_index >= len(frames):
            self.current_frame_index = 0


    def _update_player_image(self) -> None:
        """ Atualiza a imagem do player com base no frame de ataque atual. """
        self.player.image = self._get_current_frame()
        if self.player.movement_component.facing_right:
            self.player.image = pygame.transform.flip(self.player.image, True, False)
        self.player.rect = self.player.image.get_rect(centerx=self.player.rect.centerx, bottom = self.initial_rect.bottom + 6)


    def _get_current_frame(self) -> pygame.Surface:
        """ Retorna o frame atual baseado no tipo de ataque. """
        return self.player.attack_frames[self.current_frame_index] if self.attack_type == 1 else self.player.cannon_frames[self.current_frame_index]
    

    @property
    def attack_type(self) -> int:
        return self._attack_type


    def reset(self) -> None:
        self.frame_counter = 0
        self.current_frame_index = 0
        self.duration_timer = 0 