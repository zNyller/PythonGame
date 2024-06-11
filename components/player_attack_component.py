import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):
    def __init__(self, player, damage, duration, sound, event_manager):
        super().__init__()
        self.player = player
        self.damage = damage
        self.attack_duration = duration
        self.sound = sound
        self.event_manager = event_manager
        self.state = 'idle'
        self.animation_speed = 0.15
        self.animation_counter = 0
        self.current_frame_index = 0
        self.duration_counter = 0
        self.initial_rect = player.rect.copy()
        self.attack_hitbox = pygame.Rect(0, 0, 100, 50)  # Tamanho e posição inicial da hitbox
        self.hit_targets = set()


    def attack(self):
        if self.state == 'idle':
            self.state = 'attacking'
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self.sound.play()
            self.hit_targets.clear()
            self.animation_counter = 0
            self.current_frame_index = 0
            self.duration_counter = self.attack_duration
            self.player.image = self.player.attack_frames[self.current_frame_index]  # Define a primeira imagem de ataque

            # Atualiza a posição da hitbox de ataque para seguir o jogador
            self.attack_hitbox.centerx = self.player.rect.centerx
            self.attack_hitbox.bottom = self.player.rect.bottom


    def update(self, target_sprites):
        if self.state == 'attacking':
            if self.duration_counter > 0:
                self.attack_animation()
                self.perform_attack(target_sprites)
                self.duration_counter -= 1
            else:
                self.state = 'idle'
                self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
                self.duration_counter = 0


    def perform_attack(self, target_sprites):
        for target in target_sprites:
            if self.attack_hitbox.colliderect(target.rect) and target not in self.hit_targets:
                self.inflict_damage(target)
                self.hit_targets.add(target)


    def inflict_damage(self, target):
        target.reduce_life(self.damage)
        target.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': target, 'damage': self.damage})

        # Calcula a direção do recuo com base nas posições do atacante e do alvo
        direction_x = target.rect.centerx - self.player.rect.centerx
        if direction_x != 0:
            direction_x /= abs(direction_x) # Normaliza para obter -1 ou 1
        recuo_distancia = 100
        target.rect.centerx += direction_x * recuo_distancia

        if target.life <= 0:
            target.death_sound.play()
            target.kill()


    def attack_animation(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.player.attack_frames):
                self.current_frame_index = 0

        # Atualiza a imagem do jogador
        self.player.image = self.player.attack_frames[self.current_frame_index]

        # Atualiza dinamicamente a hitbox de ataque conforme o frame atual da animação
        self.update_attack_hitbox()

        # Atualiza o retângulo do jogador mantendo a base e o centro X
        self.player.rect = self.player.image.get_rect()
        self.player.rect.centerx = self.initial_rect.centerx
        self.player.rect.bottom = self.initial_rect.bottom


    def update_attack_hitbox(self):
        if self.current_frame_index < 3:  # Primeiros 3 frames (preparação)
            self.attack_hitbox = pygame.Rect(0, 0, 50, 50)  # Tamanho menor para a preparação
        elif 3 <= self.current_frame_index < 6:  # Frames de ataque
            self.attack_hitbox = pygame.Rect(0, 0, 320, 250)  # Tamanho maior para o ataque
        else:  # Últimos 3 frames (retorno)
            self.attack_hitbox = pygame.Rect(0, 0, 50, 50)  # Tamanho menor para o retorno

        # Atualiza a posição da hitbox de ataque para seguir o jogador
        self.attack_hitbox.centerx = self.player.rect.centerx
        self.attack_hitbox.bottom = self.player.rect.bottom