# Imports
import sys
import os
import cProfile
import pstats
from core.game import Game

# Adiciona o diretório raiz ao sys.path para permitir importações absolutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    #stats.print_stats()