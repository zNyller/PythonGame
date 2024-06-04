from entities.player import Player

class PlayerFactory:
    """Classe para fabricar jogadores."""

    def __init__(self, event_manager, resource_manager, sprite_manager):
        self.event_manager = event_manager
        self.resource_manager = resource_manager
        self.sprite_manager = sprite_manager
    
    def create_player(self, name):
        """
        Cria um jogador utilizando o nome fornecido e implementa dicionários com os recursos correspondentes.
        Adiciona o jogador ao grupo de sprite em sprite_manager, e por fim o retorna.
        """

        images = {
            'default': self.resource_manager.get_image('player'),
            'attacking': self.resource_manager.get_image('player_attacking')
        }
        sounds = {
            'attacking': self.resource_manager.get_sound('attack_sound'),
            'level_complete': self.resource_manager.get_sound('level_complete'),
            'jumping': self.resource_manager.get_sound('player_jump'),
            'hit': self.resource_manager.get_sound('hit_player')
        }

        player = Player(name, images, sounds, self.event_manager)
        self.sprite_manager.add_player(player)
        return player