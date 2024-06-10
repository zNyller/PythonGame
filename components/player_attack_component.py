import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):
    def __init__(self, player, damage, duration, sound, event_manager):
        self.player = player
        self.damage = damage
        self.attack_duration = duration
        self.sound = sound
        self.event_manager = event_manager
        self.state = 'idle'

        self.animation_speed = 0.15 # Controle de velocidade da animação de ataque
        self.animation_counter = 0
        self.current_frame_index = 0 # Índice atual do frame de animação
        self.duration_counter = 0 # Contador da duração do ataque
        self.inital_rect = player.rect.copy() # Mantém a posição inicial do rect do jogador


    def attack(self):
        if self.state == 'idle':
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self.state = 'attacking'
            self.player.image = self.player.attack_frames[self.current_frame_index]
            self.sound.play()
            self.animation_counter = 0 # Reseta
            self.current_frame_index = 0 # Reseta
            self.duration_counter = self.attack_duration # Inicializa o contador de duração do ataque


    def update(self):
        if self.state == 'attacking':
            if self.duration_counter > 0:
                self.attack_animation()
                self.duration_counter -= 1
            else:
                self.state = 'idle'
                self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
                self.duration_counter = 0


    def inflict_damage(self, target):
        return super().inflict_damage(target)
    

    def perform_attack(self, target_sprites):
        return super().perform_attack(target_sprites)


    def attack_animation(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.player.attack_frames):
                self.current_frame_index = 0 # Reseta o índice do frame se ultrapassar o número de frames

        # Atualiza a imagem do jogador
        self.player.image = self.player.attack_frames[self.current_frame_index]
        self.mask = pygame.mask.from_surface(self.player.image)
        
        # Ajusta o retângulo do jogador para manter o centro e a base originais
        self.player.rect = self.player.image.get_rect()
        self.player.rect.centerx = self.inital_rect.centerx  # Mantém o mesmo centro X que o retângulo inicial
        self.player.rect.bottom = self.inital_rect.bottom  # Mantém o mesmo bottom (base) que o retângulo inicial