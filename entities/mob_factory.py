from entities.mob import Mob
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


    def create_mob(self, name):
        """
        Cria um mob utilizando o nome fornecido e implementa dicionários com os recursos correspondentes.
        Configura todos os atributos necessários para o mob.
        Adiciona o mob ao grupo de sprite em sprite_manager, e por fim o retona.
        """

        # Carrega imagens e sons do ResourceManager
        images = {
            'default': self.resource_manager.get_image('mob'),
            'attacking': self.resource_manager.get_image('mob_attacking') 
        }
        sounds = {
            'blood_pop': self.resource_manager.get_sound('blood_pop'),
            'hit_player': self.resource_manager.get_sound('hit_player'),
            'scream': self.resource_manager.get_sound('mob_pain')
        }

        mob = Mob(name, images, sounds, self.event_manager)
        self.sprite_manager.add_mob(mob)
        return mob
    

    def get_mob(self, name):
        """Retorna um mob do pool, resetando-o para o estado inicial."""
        mob = self.mob_pool.get(name)
        return mob
    

    def release_mob(self, mob):
        """Libera um mob de volta para o pool de objetos."""
        self.mob_pool.release(mob)


    def notify(self, event):
        if event['type'] == 'release_mob':
            self.release_mob(event['mob'])
        if event['type'] == 'get_mob':
            return self.get_mob(event['name'])