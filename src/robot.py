"""
Robot class module
"""

from typing import Tuple

import pygame

from src.graphics import Graphics 


class Robot:
    """
    Robot object class
    """

    def __init__(self, coords: Tuple, graphics: Graphics) -> None:
        """
        Robot class constructor

        Args:
            coords (Tuple): robot coordinates
            graphics (Graphics): Graphics instance
        """
        self.texture = pygame.image.load("./assets/imgs/robot.png")                                       
        self.w = self.texture.get_width()
        self.coords = coords
        self.dtx = 0
        self.graphics = graphics

    def render(self) -> None:
        """
        Renders the robot
        """
        self.graphics.display.blit(self.texture, self.coords)