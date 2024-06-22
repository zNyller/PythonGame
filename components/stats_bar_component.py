import pygame

class StatsBarComponent:
    """ Classe para gerenciar a barra de stats do Player. """

    INTERFACE_POSITION = (20, 20)
    LIFE_BAR_POSITION = (150, 76)
    XP_BAR_POSITION = (141, 62)
    MAX_EXPERIENCE = 100

    def __init__(self, player, interface, life_bar, xp_bar, event_manager) -> None:
        self.player = player
        self.interface = interface
        self.life_bar = life_bar
        self.xp_bar = xp_bar
        self.event_manager = event_manager
        self.interface_position = self.INTERFACE_POSITION
        self.life_bar_position = self.LIFE_BAR_POSITION
        self.xp_bar_position = self.XP_BAR_POSITION
        self.max_experience = self.MAX_EXPERIENCE
        self.event_manager.subscribe('player_up', self)


    def notify(self, event):
        if event['type'] == 'player_up':
            self.max_experience *= 1.5


    def draw_stats_bar(self, screen) -> None:
        """ Desenha a interface da barra. """
        screen.blit(self.interface, self.interface_position)
        self.update_bars()
        self.draw_bars(screen)


    def update_bars(self) -> None:
        """ Atualiza a largura das barras com base nos valores atuais de vida e experiência. """
        life_width = int(self.life_bar.get_width() * (self.player.life / self.player.MAX_LIFE))
        xp_width = int(self.xp_bar.get_width() * (self.player.xp / self.max_experience))

        self.current_life_bar = pygame.transform.scale(self.life_bar, (life_width, self.life_bar.get_height()))
        self.current_xp_bar = pygame.transform.scale(self.xp_bar, (xp_width, self.xp_bar.get_height()))


    def draw_bars(self, screen) -> None:
        """ Desenha a barra de vida e de experiência com base nos valores atuais. """
        screen.blit(self.current_life_bar, self.life_bar_position)
        screen.blit(self.current_xp_bar, self.xp_bar_position)