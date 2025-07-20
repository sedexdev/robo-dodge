"""
Main game module
"""

import pygame
import time
import random

from pygame.font import Font
from typing import Tuple

# graphics
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()                                                                    

DISPLAY_WIDTH = 1250
DISPLAY_HEIGHT = 800

# rgb
black = (0, 0, 0)
white = (255, 255, 255)                                                          
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
drk_gry = (35, 35, 35)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

# graphics
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))           
pygame.display.set_caption("Robo-Dodge")                                     
ROBOT_IMG = pygame.image.load("assets/imgs/robot.png")                                       
THEME_IMG = pygame.image.load("assets/imgs/theme.jpg")

# game
CLOCK = pygame.time.Clock()                                                      

# robot
ROBO_WIDTH = 189

# game
pygame.mixer.music.load("assets/audio/theme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# grpahics
def obj_dodged(count: int) -> None:
    """
    Accumulates dodged objects & updates the UI

    Args:
        count (int): number of dodged objects
    """
    font = pygame.font.SysFont(None, 45)                                         
    text = font.render("Dodged: " + str(count), True, black)                     
    game_display.blit(text, (0, 0))

# graphics
def sm_obj(s_objx: int, s_objy: int, s_objw: int, s_objh: int, colour: Tuple) -> None:
    """
    Render a small object to the canvas 

    Args:
        s_objx (int): object x coordinate
        s_objy (int): object y coordinate
        s_objw (int): object width
        s_objh (int): object height
        colour (Tuple): object colour
    """
    pygame.draw.rect(game_display, colour, [s_objx, s_objy, s_objw, s_objh])

# graphics
def obj(objx: int, objy: int, objw: int, objh: int, colour: Tuple):
    """
    Render an object to the canvas 

    Args:
        objx (int): object x coordinate
        objy (int): object y coordinate
        objw (int): object width
        objh (int): object height
        colour (Tuple): object colour
    """                   
    pygame.draw.rect(game_display, colour, [objx, objy, objw, objh])      

# graphics
def robo(x: int, y: int):
    """
    Render the robot player object

    Args:
        x (int): object x coordinate
        y (int): object y coordinate
    """
    game_display.blit(ROBOT_IMG, (x, y))                                           

# graphics
def text_objects(text: str, font: Font) -> Tuple:
    """
    Create and return a rect for the rendered font

    Args:
        text (str): text content
        font (Font): pygame font

    Returns:
        Tuple: text render object tuple
    """
    text_surface = font.render(text, True, drk_gry)
    return text_surface, text_surface.get_rect()

# graphics
def render_msg(text: str) -> None:
    """
    Renders the given text to the canvas, updates the game
    graphics display, then runs the game loop again

    Args:
        text (str): _description_
    """
    large_text = pygame.font.Font("freesansbold.ttf", 100)                       
    TextSurf, TextRect = text_objects(text, large_text)                          
    TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 4))                
    game_display.blit(TextSurf, TextRect)                                         

    pygame.display.update()                                                      
    time.sleep(0.5)                                                                                                                                 

# graphics
def render_bkgrnd_image(x: int, y: int) -> None:
    """
    Displays the background image on the menu page

    Args:
        x (int): image x coordinate
        y (int): image y coordinate
    """
    game_display.blit(THEME_IMG, (x, y))

# button
def button(msg: str, x: int, y: int, w: int, h: int, ic: Tuple, ac: Tuple, action=None) -> None:
    """
    Handles button clicks in the game

    Args:
        msg (str): button text
        x (int): button x coordinate
        y (int): button y coordinate
        w (int): button width
        h (int): button height
        ic (Tuple): base colour
        ac (Tuple): hover colour
        action (func, optional): action function. Defaults to None.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    small_text = pygame.font.Font("freesansbold.ttf", 40)
    TextSurf, TextRect = text_objects(msg, small_text)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(TextSurf, TextRect)

# game
def quit_game() -> None:
    """
    Quit the game back to the desktop
    """
    pygame.quit()
    quit()


def game_intro() -> None:
    """
    Renders the games menu page with both menu buttons
    """
    n = 0
    m = 0

    intro = True

    while intro:
        for event in pygame.event.get():
            # game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # graphics
        render_bkgrnd_image(n, m)
        large_text = pygame.font.Font("freesansbold.ttf", 100)
        TextSurf, TextRect = text_objects("!ROBO DODGE!", large_text)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 4))
        game_display.blit(TextSurf, TextRect)

        # button
        button("PLAY!", 350, 425, 250, 100, green, bright_green, game_loop)
        button("QUIT!", 655, 425, 250, 100, red, bright_red, quit_game)

        # graphics
        pygame.display.update()

# graphics
def countdown() -> None:
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
            if event.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else "GO!"
                if text == "GO!":
                    count = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        else:
            game_display.fill(white)
            game_display.blit(font.render(text, True, black), (350, 200))
            pygame.display.update()
            CLOCK.tick(60)
            continue


def game_loop() -> None:                                                                 
    """
    Core game loop logic
    """
    x = (DISPLAY_WIDTH * 0.40)
    y = (DISPLAY_HEIGHT * 0.75)

    sm_obj_startx = random.randrange(0, DISPLAY_WIDTH)
    sm_obj_starty = -400
    SM_OBJ_SPEED = 4
    SM_OBJ_WIDTH = 50
    SM_OBJ_HEIGHT = 50

    obj_startx = random.randrange(0, DISPLAY_WIDTH)                            
    obj_starty = -600
    OBJ_SPEED = 4
    OBJ_WIDTH = 200
    OBJ_HEIGHT = 200

    x_change = 0
    dodged = 0

    countdown()
    time.sleep(1)

    game_exit = False

    while not game_exit:                                                          

        for event in pygame.event.get():                                          
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change                                                                        
        game_display.fill(white)                                                              
        sm_obj(sm_obj_startx, sm_obj_starty, SM_OBJ_WIDTH, SM_OBJ_HEIGHT, blue)
        sm_obj_starty += SM_OBJ_SPEED
        obj(obj_startx, obj_starty, OBJ_WIDTH, OBJ_HEIGHT, black)                 
        obj_starty += OBJ_SPEED                                                          
        robo(x, y)                                                                           
        obj_dodged(dodged)

        if x > DISPLAY_WIDTH - ROBO_WIDTH or x < 0:                                          
            render_msg("OUT OF BOUNDS!!")
            game_loop() 

        if obj_starty > DISPLAY_HEIGHT:                                                    
            obj_starty = 0 - OBJ_HEIGHT
            obj_startx = random.randrange(0, DISPLAY_WIDTH)
            dodged += 1
            OBJ_SPEED += 0.5
            OBJ_WIDTH += (dodged * 1.2)

        if y < obj_starty + OBJ_HEIGHT:
            if x > obj_startx and \
               x < obj_startx + OBJ_WIDTH or \
               x + ROBO_WIDTH > obj_startx and \
               x + ROBO_WIDTH < obj_startx + OBJ_WIDTH:                                  
                render_msg("YOU'RE DEAD!!")
                game_loop() 

        if sm_obj_starty > DISPLAY_HEIGHT:
            sm_obj_starty = 0 - SM_OBJ_HEIGHT
            sm_obj_startx = random.randrange(0, DISPLAY_WIDTH)
            dodged += 1
            SM_OBJ_SPEED += 0.8

        if y < sm_obj_starty + SM_OBJ_HEIGHT:
            if sm_obj_startx < x and \
               sm_obj_startx + SM_OBJ_WIDTH > x or \
               sm_obj_startx < x + ROBO_WIDTH and \
               sm_obj_startx + SM_OBJ_WIDTH > x + ROBO_WIDTH or \
               x < sm_obj_startx and x + ROBO_WIDTH > sm_obj_startx + SM_OBJ_WIDTH:
                render_msg("YOU'RE DEAD!!")
                game_loop() 

        pygame.display.update()                                                              
        CLOCK.tick(60)


game_intro()
pygame.quit()                                                                                
quit()
