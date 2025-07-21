"""
Block class module
"""

# pylint: disable=line-too-long, too-few-public-methods, too-many-arguments, too-many-positional-arguments

from typing import Tuple

import pygame

from src.graphics import Graphics


class Block:
    """
    Block object class
    """

    def __init__(self, coords: Tuple, dimensions: Tuple, colour: Tuple, speed: float, graphics: Graphics) -> None:
        """
        Block class constructor

        Args:
            coords (Tuple): block coordinates
            dimensions (Tuple): block dimensions
            colour (Tuple): block colour
            speed (float): block y axis speed
            graphics (Graphics): Graphics instance
        """
        self.coords = coords
        self.dimensions = dimensions
        self.colour = colour
        self.speed = speed
        self.graphics = graphics

    def render(self) -> None:
        """
        Renders the block
        """
        x, y = self.coords
        h, w = self.dimensions
        pygame.draw.rect(self.graphics.display, self.colour, [x, y, w, h])
