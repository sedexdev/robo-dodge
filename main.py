"""
Main game module
"""

import pygame

from src.graphics import Graphics
from src.game import Game


CLOCK = pygame.time.Clock()


def main() -> None:
    """
    Main entry function
    """
    ui = Graphics()
    ui.initialise()
    game = Game(ui)
    game.pygame_init()
    game.audio_init()
    # launch the game
    game.launch(CLOCK)


if __name__ == "__main__":
    main()
