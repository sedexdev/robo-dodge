"""
Pygame graphics module
"""

# pylint: disable=line-too-long, too-few-public-methods, too-many-arguments, too-many-positional-arguments

import sys
import time

from typing import Tuple

import pygame

from pygame import USEREVENT, QUIT
from pygame.font import Font
from pygame.time import Clock

from src.colours import BLACK, DRK_GREY, WHITE


class Graphics:
    """
    Graphics class for Pygame rendering
    """

    def __init__(self) -> None:
        """
        Game class constructor
        """
        self.width = 1250
        self.height = 800
        self.display = pygame.display.set_mode((self.width, self.height))
        self.theme_texture = pygame.image.load("./assets/imgs/theme.jpg")

    def initialise(self) -> None:
        """
        Initialise game UI
        """
        pygame.display.set_caption("RoboDodge")

    def draw_rect(self, colour: Tuple, values: Tuple) -> None:
        """
        Wrapper around the pygame.draw.rect function for
        rendering rectangular objects to the UI

        Args:
            colour (Tuple): colour
            values (Tuple): coords and dimenstions
        """
        pygame.draw.rect(self.display, colour, values)

    def render_font(self, font: Font, text: str, coords: Tuple) -> None:
        """
        Creates and renders the surface / rect for a 
        message in a given font in the UI

        Args:
            font (Font): pygame font object 
            text (str): text to render
            coords (Tuple): coordinates of font
        """
        surface = font.render(text, True, DRK_GREY)
        rect = surface.get_rect()
        rect.center = coords
        self.display.blit(surface, rect)

    def render_score(self, score: int) -> None:
        """
        Updates the UI to show the score

        Args:
            score (int): current score
        """
        font = pygame.font.SysFont(None, 45)
        text = font.render("Dodged: " + str(score), True, BLACK)
        self.display.blit(text, (0, 0))

    def render_theme(self, coords: Tuple) -> None:
        """
        Renders an image in the UI 

        Args:
            coords (Tuple): image coordinates
        """
        self.display.blit(self.theme_texture, coords)

    def update_display(self) -> None:
        """
        Wrapper around pygame display update function
        """
        pygame.display.update()

    def render_countdown(self, clock: Clock) -> None:
        """
        Starts a counter at the beginning of the game and counts
        down to the starting loop
        """
        counter, text = 3, "3".rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        font = pygame.font.Font("freesansbold.ttf", 300)

        count = False

        while not count:
            for event in pygame.event.get():
                if event.type == USEREVENT:
                    counter -= 1
                    text = str(counter).rjust(3) if counter > 0 else "GO!"
                    if text == "GO!":
                        count = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.display.fill(WHITE)
            self.display.blit(font.render(text, True, BLACK), (350, 200))
            self.update_display()
            clock.tick(60)


class Button:
    """
    Button rendering class
    """

    def __init__(self, text: str, coords: Tuple, dimensions: Tuple, ic: Tuple, ac: Tuple, graphics: Graphics, action=None) -> None:
        """
        Button class constructor

        Args:
            text (str): button text
            coords (Tuple): button coordinates
            dimensions (Tuple): button dimensions 
            ic (Tuple): normal colour
            ac (Tuple): hover colour
            graphics (Graphics): Graphics instance
            action (function, optional): onclick function. Defaults to None.
        """
        self.text = text
        self.coords = coords
        self.dimensions = dimensions
        self.ic = ic
        self.ac = ac
        self.action = action
        self.graphics = graphics

    def handle_click(self, clock: Clock) -> None:
        """
        Handles a button click
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        x, y = self.coords
        w, h = self.dimensions
        # call action function is available
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            self.render(True)
            if click[0] == 1 and self.action != None:
                if self.action.__name__ == "game_loop":
                    self.action(clock)
                else:
                    self.action()

    def render(self, hover=False) -> None:
        """
        Render the button

        Args:
            hover (bool, optional): True shows hover colour
        """
        x, y = self.coords
        w, h = self.dimensions
        if not hover:
            self.graphics.draw_rect(self.ic, (x, y, w, h))
        else:
            self.graphics.draw_rect(self.ac, (x, y, w, h))
        font = pygame.font.Font("freesansbold.ttf", 40)
        self.graphics.render_font(
            font,
            self.text,
            ((x + (w / 2)), (y + (h / 2)))
        )
