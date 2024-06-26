import pygame
from config.constants import IMAGES_DIR, SOUNDS_DIR

class ResourceManager:
    """Classe para gerenciar os recursos do jogo."""

    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.load_resources()


    def load_resources(self):
        """ Carrega imagens e sons necessários. """

        try:
            self.images['background'] = pygame.image.load(f'{IMAGES_DIR}/background.png')
            self.images['background_sized'] = pygame.image.load(f'{IMAGES_DIR}/background_sized.png')
            self.images['camping'] = pygame.image.load(f'{IMAGES_DIR}/camping.jpg')
            self.images['player'] = pygame.image.load(f'{IMAGES_DIR}/guts_size.png').convert_alpha()
            self.images['player_attacking'] = pygame.image.load(f'{IMAGES_DIR}/attack_spritesheet.png').convert_alpha()
            self.images['player_spritesheet'] = pygame.image.load(f'{IMAGES_DIR}/player_spritesheet.png').convert_alpha()
            self.images['cannon_attack'] = pygame.image.load(f'{IMAGES_DIR}/cannon_spritesheet.png').convert_alpha()
            self.images['stats_interface'] = pygame.image.load(f'{IMAGES_DIR}/stats_interface.png').convert_alpha()
            self.images['life_bar'] = pygame.image.load(f'{IMAGES_DIR}/life_bar.png').convert_alpha()
            self.images['xp_bar'] = pygame.image.load(f'{IMAGES_DIR}/xp_bar.png').convert_alpha()
            self.images['mob'] = pygame.image.load(f'{IMAGES_DIR}/mob.png').convert_alpha()
            self.images['mob_attacking'] = pygame.image.load(f'{IMAGES_DIR}/mob_attack.png').convert_alpha()

            self.sounds['attack_sound'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/attack_sound.wav')
            self.sounds['blood_pop'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/blood_pop.wav')
            self.sounds['game_over'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/game_over.wav')
            self.sounds['hit_player'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/hit_player.wav')
            self.sounds['level_complete'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/level_complete.wav')
            self.sounds['mob_pain'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/monster_pain.wav')
            self.sounds['player_jump'] = pygame.mixer.Sound(f'{SOUNDS_DIR}/player_jump.wav')
        except Exception as e:
            print(f"Erro ao carregar os recursos: {e}")
        else:
            print(f"Sucesso ao carregar os recursos!")


    def get_image(self, name):
        """Retorna uma imagem pelo nome."""
        return self.images.get(name)
    

    def get_sound(self, name):
        """Retorna um som pelo nome."""
        return self.sounds.get(name)