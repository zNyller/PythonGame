import pygame
from typing import Dict
from entities.mob import Mob
from entities.soul import Soul
from entities.troll import Troll
from utils.object_pool import ObjectPool

class MobFactory:
    """Fabrica os mobs do jogo."""

    def __init__(self, event_manager, resource_manager, sprite_manager) -> None:
        self.event_manager = event_manager
        self.resource_manager = resource_manager
        self.sprite_manager = sprite_manager
        self.mob_pool = ObjectPool(self.create_mob)
        self.event_manager.subscribe('release_mob', self)
        self.event_manager.subscribe('get_mob', self)

    def create_mob(self, name: str) -> Mob:
        """Cria um mob com base no nome fornecido.
        
        Implementa dicionários com imagens e sons específicos para o mob.
        Adiciona o mob ao grupo de sprite em sprite_manager, e por fim o retona.
        """
        return self._create_soul() if name == 'Soul' else self._create_troll()

    def notify(self, event) -> Mob | None:
        """Notifica os métodos inscritos nos eventos."""
        if event['type'] == 'release_mob':
            self._release_mob(event['mob'])
        if event['type'] == 'get_mob':
            return self._get_mob(event['name'])

    def _create_soul(self) -> Mob:
        """Cria um Soul com recursos específicos."""
        images, sounds = self._get_resources('Soul')
        soul = Soul("Soul", images, sounds, self.event_manager)
        self.sprite_manager.add_mob(soul)
        return soul

    def _create_troll(self) -> Mob:
        """ Cria um Troll com recursos específicos. """
        images, sounds = self._get_resources('Troll')
        troll = Troll('Troll', images, sounds, self.event_manager)
        self.sprite_manager.add_mob(troll)
        return troll
    
    def _get_resources(self, name: str) -> Dict[str, pygame.Surface | list]:
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
            troll_idle_spritesheet = self.resource_manager.get_image('troll_idle_spritesheet')
            troll_idle_sprites = [self.sprite_manager.get_sprite(troll_idle_spritesheet, *coords) for coords in self.sprite_manager.troll_sprite_coords]
            images = {
                'default': troll_idle_sprites,
                'attacking': troll_idle_sprites,
                'idle_frames': troll_idle_sprites
            }
            sounds = {
                'blood_pop': self.resource_manager.get_sound('blood_pop'),
                'hit_player': self.resource_manager.get_sound('hit_player'),
                'pain': self.resource_manager.get_sound('troll_pain'),
                'death': self.resource_manager.get_sound('troll_death')
            }
        return images, sounds

    def _get_mob(self, name: str) -> Mob:
        # Retorna um mob do pool, resetando-o para o estado inicial.
        return self.mob_pool.get(name)

    def _release_mob(self, mob: Mob) -> None:
        # Libera um mob de volta para o pool de objetos.
        self.mob_pool.release(mob)