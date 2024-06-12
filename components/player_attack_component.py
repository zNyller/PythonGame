import pygame
from components.attack_component import AttackComponent

class PlayerAttackComponent(AttackComponent):
    def __init__(self, player, damage, duration, sound, event_manager):
        super().__init__()
        self.player = player
        self.player_rect_x = player.rect.centerx
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
        self.attack_hitbox = pygame.Rect(0, 0, 330, 150)  # Tamanho e posição inicial da hitbox
        self.hit_targets = set()


    def attack(self):
        if self.state == 'idle':
            print("Starting attack")
            self.state = 'attacking'
            self.event_manager.notify({'type': 'player_attack', 'state': 'start'})
            self.sound.play()
            self.hit_targets.clear()
            self.animation_counter = 0
            self.current_frame_index = 0
            self.duration_counter = self.attack_duration
            self._update_player_image()
            self._update_attack_hitbox()
            print(f"Initial hitbox: {self.attack_hitbox}")


    def update(self, target_sprites):
        self.player_rect_x = self.player.rect.centerx
        if self.state == 'attacking':
            self._perform_attack(target_sprites)
            print("Updating attack state")
            self._continue_attack(target_sprites)


    def _continue_attack(self, target_sprites):
        if self.duration_counter > 0:
            self._attack_animation()
            self._perform_attack(target_sprites)
            self.duration_counter -= 1
        else:
            self._reset_to_idle()


    def _reset_to_idle(self):
        self.state = 'idle'
        self.event_manager.notify({'type': 'player_attack', 'state': 'end'})
        self.duration_counter = 0


    def _perform_attack(self, target_sprites):
        if self.duration_counter == self.attack_duration:  # Primeiro frame do ataque
            self._update_attack_hitbox()  # Assegure-se de que a hitbox esteja atualizada no primeiro frame

        for target in target_sprites:
            if self.attack_hitbox.colliderect(target.rect) and target not in self.hit_targets:
                print(f"Inflicting damage on target: {target}")
                self._inflict_damage(target)
                self.hit_targets.add(target)


    def _inflict_damage(self, target):
        print(f"Inflicting {self.damage} damage on target")
        target.reduce_life(self.damage)
        target.receive_damage_sound.play()
        self.event_manager.notify({'type': 'damage_event', 'target': target, 'damage': self.damage})

        # Atualiza a posição do alvo aplicando um recuo
        if target.rect.centerx <= self.player_rect_x:
            target.rect.centerx -= 90
        else:
            target.rect.centerx += 90

        if target.life <= 0:
            target.death_sound.play()
            target.kill()
            if hasattr(target, 'xp_points'):
                self.event_manager.notify({
                    'type': 'mob_defeated', 
                    'xp_points': target.xp_points
                })


    def _attack_animation(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.player.attack_frames):
                self.current_frame_index = 0

        self._update_player_image()
        self._update_attack_hitbox()


    def _update_player_image(self):
        self.player.image = self.player.attack_frames[self.current_frame_index]
        self.player.rect = self.player.image.get_rect()
        self.player.rect.centerx = self.initial_rect.centerx
        self.player.rect.bottom = self.initial_rect.bottom


    def _update_attack_hitbox(self):
        if self.current_frame_index < 3:  # (preparação)
            self.attack_hitbox = pygame.Rect(0, 0, 50, 50)
        elif 3 <= self.current_frame_index < 6:  # (ataque)
            self.attack_hitbox = pygame.Rect(0, 0, 330, 250)
        else:  # (retorno)
            self.attack_hitbox = pygame.Rect(0, 0, 50, 50)

        self.attack_hitbox.centerx = self.player.rect.centerx
        self.attack_hitbox.bottom = self.player.rect.bottom
        print(f"Updated hitbox: {self.attack_hitbox}")