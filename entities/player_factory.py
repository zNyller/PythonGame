from typing import Any, Dict, TYPE_CHECKING
from entities.player import Player

if TYPE_CHECKING:
    from pygame.surface import Surface
    from pygame.mixer import Sound
    from managers.event_manager import EventManager
    from managers.resource_manager import ResourceManager
    from managers.sprite_manager import SpriteManager

class PlayerFactory:
    """Classe para fabricar jogadores."""

    def __init__(
            self: 'PlayerFactory', 
            event_manager: 'EventManager', 
            resource_manager: 'ResourceManager', 
            sprite_manager: 'SpriteManager'
        ) -> None:
        """Inicializa os managers necessários para a criação do Player."""
        self.event_manager = event_manager
        self.resource_manager = resource_manager
        self.sprite_manager = sprite_manager
        self.event_manager.subscribe(event_type='create_player', listener=self)

    def create_player(self) -> Player:
        """Cria um novo jogador.
        
        Implementa dicionários com os recursos correspondentes.
        Adiciona o jogador ao grupo de sprite em sprite_manager, e por fim o retorna.
        """
        images = self._load_images()
        sounds = self._load_sounds()
        player = Player(images, sounds, self.event_manager)
        self.sprite_manager.add_player(player)
        return player

    def notify(self, event: Dict[str, Any]) -> Player | None:
        """Chama os métodos inscritos no tipo do evento recebido."""
        if event['type'] == 'create_player':
            return self.create_player()
        
    def _load_images(self) -> Dict[str, 'Surface']:
        spritesheet = self.resource_manager.get_image('player_spritesheet')
        attack_spritesheet = self.resource_manager.get_image('player_attacking')
        cannon_attack = self.resource_manager.get_image('cannon_attack')
        player_sprites = [
            self.sprite_manager.get_sprite(spritesheet, *coords) 
            for coords in self.sprite_manager.player_sprite_coords
        ]
        attack_sprites = [
            self.sprite_manager.get_sprite(attack_spritesheet, *coords) 
            for coords in self.sprite_manager.attack_sprite_coords
        ]
        cannon_sprites = [
            self.sprite_manager.get_sprite(cannon_attack, *coords) 
            for coords in self.sprite_manager.cannon_attack_coords
        ]
        return {
            'default': player_sprites,
            'attacking': attack_sprites,
            'cannon': cannon_sprites,
            'stats_interface': self.resource_manager.get_image('stats_interface'),
            'life_bar': self.resource_manager.get_image('life_bar'),
            'xp_bar': self.resource_manager.get_image('xp_bar')
        }
    
    def _load_sounds(self) -> Dict[str, 'Sound']:
        return {
            'attacking': self.resource_manager.get_sound('attack_sound'),
            'attacking2': self.resource_manager.get_sound('attack_sound_2'),
            'cannon' : self.resource_manager.get_sound('cannon_sound'),
            'game_over': self.resource_manager.get_sound('game_over'),
            'hit': self.resource_manager.get_sound('hit_player'),
            'jumping': self.resource_manager.get_sound('player_jump'),
            'level_complete': self.resource_manager.get_sound('level_complete')
        }