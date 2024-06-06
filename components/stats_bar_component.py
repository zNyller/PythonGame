import pygame

class StatsBarComponent:
    MAX_EXPERIENCE = 100
    def __init__(self, player, interface, life_bar, xp_bar):
        self.player = player
        self.interface = interface
        self.life_bar = life_bar
        self.xp_bar = xp_bar


    def draw_stats_bar(self, screen):
        # Desenha a interface da barra
        screen.blit(self.interface, (20, 20))

        # Calcula a largura das barras com base nos valores atuais
        life_width = int(self.life_bar.get_width() * (self.player.life / self.player.MAX_LIFE))
        xp_width = int(self.xp_bar.get_width() * (self.player.xp / self.MAX_EXPERIENCE))

        # Cria novas superficies para as barras com o tamanho calculado
        current_life_bar = pygame.transform.scale(self.life_bar, (life_width, self.life_bar.get_height()))
        current_xp_bar = pygame.transform.scale(self.xp_bar, (xp_width, self.xp_bar.get_height()))

        # Desenha as barras
        screen.blit(current_life_bar, (150, 76)) # 169, 82
        screen.blit(current_xp_bar, (141, 62)) # 157, 66