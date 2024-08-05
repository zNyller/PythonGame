import pygame
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from entities.soul import Soul
from entities.troll import Troll
from utils.object_pool import ObjectPool

if TYPE_CHECKING:
    from managers.event_manager import EventManager
    from managers.resource_manager import ResourceManager
    from managers.sprite_manager import SpriteManager
    from entities.mob import Mob

class MobFactory:
    """Fabrica os mobs do jogo."""
    def __init__(
            self, 
            event_manager: 'EventManager', 
            resource_manager: 'ResourceManager', 
            sprite_manager: 'SpriteManager'
        ) -> None:
        """Inicializa a factory para criação de mobs."""
        self.event_manager = event_manager
        self.resource_manager = resource_manager
        self.sprite_manager = sprite_manager
        self.mob_pool = ObjectPool(self.create_mob)
        self.event_manager.subscribe('release_mob', self)
        self.event_manager.subscribe('get_mob', self)

    def create_mob(self, name: str) -> 'Mob':
        """Cria um mob com base no nome fornecido.
        
        Implementa dicionários com imagens e sons específicos para o mob.
        Adiciona o mob ao grupo de sprite em sprite_manager, e por fim o retona.
        """
        return self._create_soul() if name == 'Soul' else self._create_troll()

    def notify(self, event: Dict[str, Any]) -> Optional['Mob']:
        """Notifica os métodos inscritos nos eventos."""
        if event['type'] == 'release_mob':
            self._release_mob(event['mob'])
        elif event['type'] == 'get_mob':
            return self._get_mob(event['name'])
        return None

    def _create_soul(self) -> 'Mob':
        # Cria um Soul com recursos específicos e o retorna.
        images, sounds = self._get_resources('Soul')
        soul = Soul("Soul", images, sounds, self.event_manager)
        self.sprite_manager.add_mob(soul)
        return soul

    def _create_troll(self) -> 'Mob':
        # Cria um Troll com recursos específicos e o retorna.
        images, sounds = self._get_resources('Troll')
        troll = Troll('Troll', images, sounds, self.event_manager)
        self.sprite_manager.add_mob(troll)
        return troll
    
    def _get_resources(self, name: str) -> Dict[str, pygame.Surface | list]:
        # Obtém os recursos necessários para criar o mob.
        if name == 'Soul':
            images = {
                'default': self.resource_manager.get_image('soul_default'),
                'attacking': self.resource_manager.get_image('soul_attacking')
            }
            sounds = {
                'blood_pop': self.resource_manager.get_sound('blood_pop'),
                'hit_player': self.resource_manager.get_sound('hit_player'),
                'scream': self.resource_manager.get_sound('mob_pain')
            }
        else:
            images = self._get_troll_images()
            sounds = {
                'blood_pop': self.resource_manager.get_sound('blood_pop'),
                'hit_player': self.resource_manager.get_sound('hit_player'),
                'pain': self.resource_manager.get_sound('troll_pain'),
                'death': self.resource_manager.get_sound('troll_death')
            }
        return images, sounds
    
    def _get_troll_images(self) -> Dict[str, list]:
        # Obtém as imagens específicas do Troll.
        troll_spritesheets = {
            'idle': self.resource_manager.get_image('troll_idle_spritesheet'),
            'attack': self.resource_manager.get_image('troll_attack_spritesheet'),
            'damage': self.resource_manager.get_image('troll_damage_spritesheet'),
            'death': self.resource_manager.get_image('troll_death_spritesheet'),
            'spawn': self.resource_manager.get_image('troll_spawn_spritesheet')
        }
        troll_sprites = {
            'idle_frames': self._get_sprites(troll_spritesheets['idle'], 'idle'),
            'attack_frames': self._get_sprites(troll_spritesheets['attack'], 'attack'),
            'damage_frames': self._get_sprites(troll_spritesheets['damage'], 'damage'),
            'death_frames': self._get_sprites(troll_spritesheets['death'], 'death'),
            #'spawn_frames': self._get_sprites(troll_spritesheets['spawn'], 'spawn')
        }
        return troll_sprites

    def _get_sprites(
            self, 
            spritesheet: pygame.Surface, 
            animation_type: str
        ) -> List[pygame.Surface]:
        # Extrai sprites de um spritesheet com base no tipo de animação fornecido.
        coords = self.sprite_manager.troll_sprite_coords.get(animation_type, [])
        if not coords:
            raise ValueError(f'Coordenadas não encontradas para {animation_type}')
        return [
            self.sprite_manager.get_sprite(spritesheet, *coord) for coord in coords
        ]

    def _get_mob(self, name: str) -> 'Mob':
        return self.mob_pool.get(name)

    def _release_mob(self, mob: 'Mob') -> None:
        self.mob_pool.release(mob)