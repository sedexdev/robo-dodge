"""
Game logic module
"""

import random
import sys
import time

import pygame

from pygame import KEYDOWN, KEYUP, K_LEFT, K_RIGHT, QUIT
from pygame.font import Font
from pygame.time import Clock

from src.block import Block
from src.graphics import Button, Graphics
from src.robot import Robot

from src.colours import BLACK, BLUE, BRT_GREEN, BRT_RED, GREEN, RED, WHITE


class Game:
    """
    Pygame game logic and loop class
    """

    def __init__(self, graphics: Graphics) -> None:
        """
        Game class constructor

        Args:
            graphics (Gaphics): Graphics instance
        """
        self.score = 0
        self.graphics = graphics

    def pygame_init(self) -> None:
        """
        Initialise Pygame
        """
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

    def audio_init(self) -> None:
        """
        Initialise audio components
        """
        pygame.mixer.music.load("./assets/audio/theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def launch(self, clock: Clock) -> None:
        """
        Renders the games menu page with both menu buttons

        Args:
            clock (Clock): pygame clock
        """
        x, y = (0, 0)
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()

            self.graphics.render_theme((x, y))
            font = pygame.font.Font("freesansbold.ttf", 100)
            self.graphics.render_font(
                font,
                "!ROBO DODGE!",
                ((self.graphics.width / 2), (self.graphics.height / 4))
            )

            play_btn = Button("PLAY!", (350, 425), (250, 100),
                              GREEN, BRT_GREEN, self.graphics, self.game_loop)
            quit_btn = Button("QUIT!", (655, 425), (250, 100),
                              RED, BRT_RED, self.graphics, self.quit)
            buttons = [play_btn, quit_btn]
            for btn in buttons:
                btn.render()
                btn.handle_click(clock)

            self.graphics.update_display()

    def game_loop(self, clock: Clock) -> None:
        """
        Game loop logic

        Args:
            clock (Clock): pygame clock
        """
        self.score = 0
        x, y = ((self.graphics.width * 0.40), (self.graphics.height * 0.75))

        player = Robot((x, y), self.graphics)
        sm_block = Block(
            (random.randrange(0, self.graphics.width), -400),
            (50, 50), BLUE, 4, self.graphics)
        block = Block(
            (random.randrange(0, self.graphics.width), -600),
            (200, 200), BLACK, 4, self.graphics
        )
        font = pygame.font.Font("freesansbold.ttf", 100)

        self.graphics.render_countdown(clock)
        time.sleep(0.2)

        game_exit = False

        while not game_exit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        player.dx = -8
                    if event.key == K_RIGHT:
                        player.dx = 8

            player.coords = (player.coords[0] + player.dx, player.coords[1])
            self.graphics.display.fill(WHITE)
            sm_block.render()
            sm_block_x, sm_block_y = sm_block.coords
            sm_block.coords = (sm_block_x, (sm_block_y + sm_block.speed))
            block.render()
            block_x, block_y = block.coords
            block.coords = (block_x, (block_y + block.speed))
            player.render()
            self.graphics.render_score(self.score)

            # check for out of bounds
            self.handle_out(player, self.graphics, font, clock)

            # reposition blocks if they go off screen
            self.block_reset(sm_block, self.graphics, 0.5)
            self.block_reset(block, self.graphics, 0.3)

            # check for player death
            self.handle_block_collision(player, sm_block, font, clock)
            self.handle_block_collision(player, block, font, clock)

            self.graphics.update_display()
            clock.tick(60)

    def handle_out(self, robot: Robot, graphics: Graphics, font: Font, clock: Clock) -> None:
        """
        Checks for and handles an out-of-bounds
        collision

        Args:
            robot (Robot): Robot player instance
            graphics (Graphics): Graphics instance
            font (Font): text font
            clock (Clock): pygame clock
        """
        x, _ = robot.coords
        if (x + robot.w) > graphics.width or x < 0:
            graphics.render_font(
                font,
                "OUT OF BOUNDS!",
                ((graphics.width / 2), (graphics.height / 4))
            )
            self.graphics.update_display()
            time.sleep(0.5)
            self.game_loop(clock)

    def handle_block_collision(self, robot: Robot, block: Block, font: Font, clock: Clock) -> None:
        """
        Checks for an handles block / player collisions

        Args:
            robot (Robot): Robot player instance
            block (Block): Block instance
            font (Font): text font
            clock (Clock): pygame clock
        """
        rx, ry = robot.coords
        bx, by = block.coords
        bw, bh = block.dimensions
        if (rx > bx + bw) or (bx > rx + robot.w):
            return
        if (ry > by + bh) or (by > ry + robot.h):
            return
        self.graphics.render_font(
            font,
            "DEAD!",
            ((self.graphics.width / 2), (self.graphics.height / 4))
        )
        self.graphics.update_display()
        time.sleep(0.5)
        self.game_loop(clock)

    def block_reset(self, block: Block, graphics: Graphics, dy: float) -> None:
        """
        Checks for and resets the blocks position. Also
        updates bock speed on respawn

        Args:
            block (Block): Block instance
            graphics (Graphics): Graphics instance
            dy (float): change in speed on y axis
        """
        x, y = block.coords
        if y > graphics.height:
            _, h = block.dimensions
            x = random.randrange(0, graphics.width)
            y = 0 - h
            block.coords = (x, y)
            self.score += 1
            block.speed += dy

    def quit(self) -> None:
        """
        Quit the game
        """
        pygame.quit()
        sys.exit()
