"""
Game logic module
"""

import random
import time

import pygame

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
                if event.type == pygame.QUIT:
                    self.quit()

            self.graphics.render_theme((x, y))
            font = pygame.font.Font("freesansbold.ttf", 100)
            self.graphics.render_font(
                font, 
                "!ROBO DODGE!", 
                ((self.graphics.width / 2), (self.graphics.height / 4))
            )

            play_btn = Button("PLAY!", (350, 425), (250, 100), GREEN, BRT_GREEN, self.graphics, self.game_loop)
            quit_btn = Button("QUIT!", (655, 425), (250, 100), RED, BRT_RED, self.graphics, self.quit)
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
        x, y = ((self.graphics.width * 0.40), (self.graphics.height * 0.75))

        player = Robot((x, y), self.graphics)
        sm_block = Block((random.randrange(0, self.graphics.width), -400), (50, 50), BLUE, 4, self.graphics)
        block = Block((random.randrange(0, self.graphics.width), -600), (200, 200), BLACK, 4, self.graphics)
        font = pygame.font.Font("freesansbold.ttf", 100)  

        self.graphics.render_contdown(clock)
        time.sleep(1)

        exit = False

        while not exit:
            for event in pygame.event.get():                                          
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.dtx = -5
                    if event.key == pygame.K_RIGHT:
                        player.dtx = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.dtx = 0

            player.coords = (player.coords[0] + player.dtx, player.coords[1])                                                                       
            self.graphics.display.fill(WHITE)
            sm_block.render()
            sm_block_x, sm_block_y = sm_block.coords 
            sm_block.coords = (sm_block_x, (sm_block_y + sm_block.speed))
            block.render()
            block_x, block_y = block.coords
            block.coords = (block_x, (block_y + block.speed))  
            player.render()                                                                           
            self.graphics.render_score(self.score)

            if x > self.graphics.width - player.w or x < 0:
                self.graphics.render_font(
                    font,
                    "OUT OF BOUNDS!",
                    ((self.graphics.width / 2), (self.graphics.height / 4))
                )
                pygame.display.update()                                                      
                time.sleep(0.5) 
                self.game_loop(clock) 

            sm_block_w, sm_block_h = sm_block.dimensions
            block_w, block_h = block.dimensions

            if block_y > self.graphics.height:                                                    
                block_y = 0 - block_h
                block_x = random.randrange(0, self.graphics.width)
                self.score += 1
                block.speed += 0.5
                block_w += (self.score * 1.2)

            if y < block_y + block_h:
                if x > block_x and \
                x < block_x + block_w or \
                x + player.w > block_x and \
                x + player.w < block_x + block_w:                                  
                    self.graphics.render_font(
                        font,
                        "OUT OF BOUNDS!",
                        ((self.graphics.width / 2), (self.graphics.height / 4))
                    )
                    self.game_loop(clock) 

            if sm_block_y > self.graphics.height:
                sm_block_y = 0 - sm_block_h
                sm_block_x = random.randrange(0, self.graphics.width)
                self.score += 1
                sm_block.speed += 0.8

            if y < sm_block_y + sm_block_h:
                if sm_block_x < x and \
                sm_block_x + sm_block_w > x or \
                sm_block_x < x + player.w and \
                sm_block_x + sm_block_w > x + player.w or \
                x < sm_block_x and x + player.w > sm_block_x + sm_block_w:
                    self.graphics.render_font(
                        font,
                        "DEAD!",
                        ((self.graphics.width / 2), (self.graphics.height / 4))
                    )
                    self.game_loop(clock) 

            pygame.display.update()                                                              
            clock.tick(60)

    def quit(self) -> None:
        """
        Quit the game
        """
        pygame.quit()
        quit()
