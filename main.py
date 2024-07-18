# Imports
import cProfile
import pstats
from core.game import Game


def main() -> None:
    """Função principal. Chama o método run de Game para iniciar o jogo."""
    game = Game()
    game.run()


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    #stats.print_stats()