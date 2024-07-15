from entities.mob import Mob
from entities.soul import Soul
from entities.troll import Troll
from utils.object_pool import ObjectPool

class MobFactory:
    """Classe para fabricar mobs."""

    def __init__(self, event_manager, resource_manager, sprite_manager):
        self.event_manager = event_manager
        self.resource_manager = resource_manager
        self.sprite_manager = sprite_manager
        self.mob_pool = ObjectPool(self.create_mob)
        self.event_manager.subscribe('release_mob', self)
        self.event_manager.subscribe('get_mob', self)


    def create_mob(self, name: str) -> Mob:
        """Cria um mob utilizando o nome fornecido e implementa dicionários com os recursos correspondentes.

        Configura todos os atributos necessários para o mob.
        Adiciona o mob ao grupo de sprite em sprite_manager, e por fim o retona.
        """
        return self._create_soul() if name == 'Soul' else self._create_troll()
    

    def notify(self, event):
        """ Notifica os métodos inscritos nos eventos. """
        if event['type'] == 'release_mob':
            self._release_mob(event['mob'])
        if event['type'] == 'get_mob':
            return self._get_mob(event['name'])
        

    def _create_soul(self) -> Mob:
        """ Cria uma Soul com configurações específicas. """
        images = {
            'default': self.resource_manager.get_image('soul_default'),
            'attacking': self.resource_manager.get_image('soul_attacking'), 
        }
        sounds = {
            'blood_pop': self.resource_manager.get_sound('blood_pop'),
            'hit_player': self.resource_manager.get_sound('hit_player'),
            'scream': self.resource_manager.get_sound('mob_pain')
        }
        soul = Soul("Soul", images, sounds, self.event_manager)
        self.sprite_manager.add_mob(soul)
        return soul
    

    def _create_troll(self) -> Mob:
        """ Cria um Troll com configurações específicas. """
        troll_spritesheet = self.resource_manager.get_image('troll_idle')
        troll_sprites = [self.sprite_manager.get_sprite(troll_spritesheet, *coords) for coords in self.sprite_manager.troll_sprite_coords]
        images = {
            'default': troll_sprites,
            'attacking': troll_sprites,
            'idle_frames': troll_sprites
        }
        sounds = {
            'blood_pop': self.resource_manager.get_sound('blood_pop'),
            'hit_player': self.resource_manager.get_sound('hit_player'),
            'pain': self.resource_manager.get_sound('troll_pain'),
            'death': self.resource_manager.get_sound('troll_death')
        }
        troll = Troll('Troll', images, sounds, self.event_manager)
        self.sprite_manager.add_mob(troll)
        return troll


    def _get_mob(self, name: str) -> Mob:
        """Retorna um mob do pool, resetando-o para o estado inicial."""
        return self.mob_pool.get(name)
    

    def _release_mob(self, mob: Mob) -> None:
        """Libera um mob de volta para o pool de objetos."""
        self.mob_pool.release(mob)