import pygame

class StatsBarComponent:
    MAX_EXPERIENCE = 100
    def __init__(self, player, interface, life, xp):
        self.player = player
        self.interface = interface
        self.life = life
        self.xp = xp


    def draw_stats_bar(self, screen):
        # Desenha a interface da barra
        screen.blit(self.interface, (20, 20))

        # Calcula a largura das barras com base nos valores atuais
        life_width = int(self.life.get_width() * (self.player.life / self.player.MAX_LIFE))
        xp_width = int(self.xp.get_width() * (self.player.xp / self.MAX_EXPERIENCE))

        # Cria novas superficies para as barras com o tamanho calculado
        life_bar = pygame.transform.scale(self.life, (life_width, self.life.get_height()))
        xp_bar = pygame.transform.scale(self.xp, (xp_width, self.xp.get_height()))

        # Desenha as barras
        screen.blit(life_bar, (150, 76)) # 169, 82
        screen.blit(xp_bar, (141, 62)) # 157, 66