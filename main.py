# Imports
import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importações absolutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()