import pygame
from typing import Any, Dict, Optional
from managers.resource_manager import ResourceManager
from managers.event_manager import EventManager
from entities.player import Player
from entities.mob import Mob
from core.camera import Camera

class SpriteManager:
    """Gerencia os sprites do jogo."""
    
    PLAYER_SPRITE_COORDS = [
        (5, 8, 290, 148),    # Sprite 1 (1ª linha, 1ª coluna)
        (302, 6, 290, 150),  # Sprite 2 (1ª linha, 2ª coluna)
        (5, 162, 290, 152),  # Sprite 3 (2ª linha, 1ª coluna)
        (300, 164, 290, 150),# Sprite 4 (2ª linha, 2ª coluna)
        (5, 324, 290, 148),  # Sprite 5 (3ª linha, 1ª coluna)
    ]
    ATTACK_SPRITE_COORDS = [
        (272, 70, 270, 150), # [1/1] 
        (830, 40, 270, 180), # [2/1] 
        (1300, 0, 255, 222), # [3/1]
        (0, 280, 398, 156), # [1/2]
        (562, 226, 394, 218), # [2/2]
        (1105, 280, 398, 156), # [3/2]
        (248, 442, 255, 222), # [1/3]
        (830, 480, 270, 180), # [2/3]
        (1378, 512, 270, 150) # [3/3]
    ]
    CANNON_ATTACK_COORDS = [
        (386, 188, 298, 151), # [1/1]
        (1196, 186, 298, 154), # [2/1]
        (2016, 162, 298, 178), # [3/1]
        (2820, 162, 318, 178), # [4/1]
        (376, 620, 334, 168), # [1/2]
        (1180, 624, 339, 168), # [2/2]
        (1992, 624, 339, 168), # [3/2]
        (2800, 624, 341, 168), # [4/2]
        (375, 1078, 339, 160), # [1/3]
        (1184, 1079, 339, 160), # [2/3]
        (2007, 1079, 324, 160), # [3/3]
        (2816, 1078, 324, 160), # [4/3]
        (389, 1530, 324, 159), # [1/4]
        (1198, 1530, 324, 159), # [2/4]
        (2009, 1530, 324, 159), # [3/4]
        (2728, 1516, 462, 165), # [4/4]
        (300, 1977, 460, 165), # [1/5]
        (1052, 1971, 537, 162), # [2/5]
        (1863, 1977, 537, 162), # [3/5]
        (2630, 1924, 582, 216), # [4/5]
        (194, 2367, 603, 225), # [1/6]
        (948, 2367, 663, 225), # [2/6]
        (1738, 2364, 681, 228), # [3/6]
        (2529, 2372, 696, 216), # [4/6]
        (74, 2829, 716, 210), # [1/7]
        (861, 2825, 746, 212), # [2/7]
        (1646, 2827, 771, 210), # [3/7]
        (2445, 2819, 723, 216), # [4/7]
        (9, 3260, 684, 226), # [1/8]
        (822, 3258, 678, 231), # [2/8]
        (1629, 3256, 675, 231), # [3/8]
        (2817, 3338, 297, 150), # [4/8]
    ]
    TROLL_SPRITE_COORDS = [
        (6, 34, 186, 108),
        (208, 31, 180, 111),
        (8, 178, 178, 113),
        (208, 176, 175, 115),
        (8, 324, 177, 119),
        (207, 321, 175, 121),
        (6, 474, 175, 118),
        (208, 476, 177, 115)
    ]
    TROLL_DAMAGE_COORDS = [
        (34, 32, 175, 107),
        (270, 4, 194, 136),
        (12, 245, 193, 133),
        (268, 239, 198, 142),
        (11, 486, 194, 136)
    ]
    TROLL_DEATH_COORDS = [
        (48, 69, 191, 132),
        (304, 69, 190, 133),
        (559, 69, 190, 133),
        (813, 69, 190, 133),
        (1066, 69, 189, 133),
        (48, 304, 190, 133),
        (304, 304, 190, 133),
        (559, 304, 190, 133),
        (813, 304, 190, 130),
        (1066, 304, 190, 128),
        (48, 552, 190, 128),
        (304, 552, 191, 128),
        (559, 552, 192, 128),
        (813, 552, 190, 128),
        (1066, 552, 194, 130),
        (48, 815, 190, 130),
        (304, 815, 190, 130),
        (559, 815, 190, 130),
        (813, 815, 190, 130),
        (1066, 815, 190, 130)
    ]

    def __init__(
            self: 'SpriteManager', 
            resource_manager: ResourceManager, 
            event_manager: EventManager
        ) -> None:
        """Inicializa os grupos de sprites."""
        self.event_manager = event_manager
        self.resource_manager = resource_manager
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.player_sprite_coords = self.PLAYER_SPRITE_COORDS
        self.attack_sprite_coords = self.ATTACK_SPRITE_COORDS
        self.cannon_attack_coords = self.CANNON_ATTACK_COORDS
        self.troll_sprite_coords = self.TROLL_SPRITE_COORDS
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_manager.subscribe('get_mob_sprites', self)
        self.event_manager.subscribe('get_player_sprites', self)

    def add_player(self, player: Player) -> None:
        """ Adiciona o player aos grupos de sprites. """
        self.player_sprites.add(player)
        self.all_sprites.add(player)

    def add_mob(self, mob: Mob) -> None:
        """ Adiciona um mob ao grupo de mobs e grupo de todos os sprites. """
        self.mob_sprites.add(mob)
        self.all_sprites.add(mob)

    def draw_all(self, screen: pygame.Surface, camera: Camera) -> None:
        """Desenha os sprites e seus elementos na tela."""
        for entity in self.all_sprites:
            screen.blit(entity.image, camera.apply(entity))
            if hasattr(entity, 'draw_stats_bar'):
                entity.draw_stats_bar(screen)
            elif hasattr(entity, 'draw_life_bar'):
                entity.draw_life_bar(screen, camera)
    
    def update_all(self, delta_time: float) -> None:
        """ Chama o método update das entidades. """
        self.player_sprites.update(delta_time)
        self.mob_sprites.update(delta_time)

    def get_sprite(
            self, 
            spritesheet: pygame.Surface, 
            x: int, 
            y: int, 
            width: int, 
            height: int
        ) -> pygame.Surface:
        """Retorna uma superfície (sprite) recortada do spritesheet nas coordenadas (x, y)."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(spritesheet, (0, 0), (x, y, width, height))
        return sprite
    
    def get_player_sprites(self) -> pygame.sprite.Group:
        return self.player_sprites
    
    def get_mob_sprites(self) -> pygame.sprite.Group:
        return self.mob_sprites
    
    def notify(self, event: Dict[str, Any]) -> Optional[pygame.Surface]:
        """Chama os métodos inscritos no tipo do evento recebido."""
        if event['type'] == 'get_mob_sprites':
            return self.get_mob_sprites()
        elif event['type'] == 'get_player_sprites':
            return self.get_player_sprites()
    
    def reset_game(self) -> None:
        """Reseta o estado das entidades e gera um novo mob."""
        print('\n Reset... \n')
        self._reset_player()
        self._release_mobs()
        self._get_new_mobs()

    def _reset_player(self) -> None:
        if not self.player_sprites:
            self.event_manager.notify({'type': 'create_player'})
        else:
            for player in self.player_sprites:
                player.reset()

    def _release_mobs(self) -> None:
        for mob in self.mob_sprites:
            self.event_manager.notify({'type': 'release_mob', 'mob': mob})
            mob.kill()

    def _get_new_mobs(self) -> None:
        mob_types = ['Soul', 'Troll']
        new_mobs = [self.event_manager.notify({'type': 'get_mob', 'name': mob}) for mob in mob_types]
        for mob in new_mobs:
            self.add_mob(mob)