import pygame
from config.constants import IMAGES_DIR, SOUNDS_DIR

class ResourceManager:
    """Gerencia os recursos do jogo."""

    def __init__(self) -> None:
        """Inicializa os dicionários para armazenar imagens e sons."""
        self.images = {}
        self.sounds = {}
        self.file_paths = {
            'images': {
                # Scenario
                'background': 'background_2_sized.png',
                # Player
                'player_attacking': 'attack_spritesheet.png',
                'player_spritesheet': 'player_spritesheet.png',
                'cannon_attack': 'cannon_spritesheet.png',
                'stats_interface': 'stats_interface.png',
                'life_bar': 'life_bar.png',
                'xp_bar': 'xp_bar.png',
                # Enemy
                'soul_default': 'soul_1.png',
                'soul_attacking': 'soul_attacking.png',
                'troll_idle_spritesheet': 'troll_idle_spritesheet.png',
                'troll_damage_spritesheet': 'troll_damage_spritesheet.png',
                'troll_death_spritesheet': 'troll_death_spritesheet.png',
                'troll_spawn_spritesheet': 'troll_spawn_spritesheet.png'
            },
            'sounds': {
                # Player
                #'attack_sound': 'attack_sound.wav',
                'attack_sound': 'zoio1.wav',
                'attack_sound_2': 'zoio2.wav',
                'cannon_sound': 'zoio3.wav',
                'player_jump': 'player_jump.wav',
                # Enemy
                'blood_pop': 'blood_pop.wav',
                'game_over': 'game_over.wav',
                'hit_player': 'hit_player.wav',
                'level_complete': 'level_complete.wav',
                'mob_pain': 'monster_pain.wav',
                'troll_pain': 'troll_pain.wav',
                'troll_death': 'troll_death.wav'
            }
        }
        self.load_resources()

    def load_resources(self) -> None:
        """Carrega imagens e sons necessários e armazena nos dicionários."""
        try:
            self._load_images()
            self._load_sounds()
        except FileNotFoundError as e:
            print(f"Erro: {e} - Arquivo não encontrado.")
        else:
            print(f"Sucesso ao carregar os recursos!")

    def _load_images(self) -> None:
        for name, file in self.file_paths['images'].items():
            image = pygame.image.load(f'{IMAGES_DIR}/{file}')
            self.images[name] = image.convert_alpha() if name != 'background' else image.convert()

    def _load_sounds(self) -> None:
        for name, file in self.file_paths['sounds'].items():
            self.sounds[name] = pygame.mixer.Sound(f'{SOUNDS_DIR}/{file}')

    def get_image(self, name: str) -> pygame.Surface:
        """Retorna uma imagem com base no 'name'."""
        return self.images.get(name)

    def get_sound(self, name: str) -> pygame.mixer.Sound:
        """Retorna um som com base no 'name'."""
        return self.sounds.get(name)