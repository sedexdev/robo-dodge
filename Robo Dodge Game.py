import pygame
import time
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()                                                                    # initialises the pygame module

DISPLAY_WIDTH = 1250
DISPLAY_HEIGHT = 900

black = (0, 0, 0)
white = (255, 255, 255)                                                          # the RGB colour spectrum has 256 possible colours, white is the max of the RGB spectrum (excluding 0 which is black) (256 - 1 = 255)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
drk_gry = (35, 35, 35)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))           # this is setting the dimensions of the game window/surface; can be referenced later to change display
pygame.display.set_caption("!!Robo-Dodge!!")                                     # sets the title for the game window (game name)
CLOCK = pygame.time.Clock()                                                      # sets the in game clock
ROBO_IMG = pygame.image.load("Robot2.png")                                       # loads the character image
BACKGROUND_IMAGE = pygame.image.load("Robot_FACE.jpg")
ROBO_WIDTH = 189

pygame.mixer.music.load("06 Taylor Rain.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def things_dodged(count):
    font = pygame.font.SysFont(None, 45)                                         # uses default system font (name, size)
    text = font.render("Dodged: " + str(count), True, black)                     # renders the text onto the window/surface (message, Anti-Aliasing, colour)
    gameDisplay.blit(text, (0, 0))


def small_things(s_thingx, s_thingy, s_thingw, s_thingh, colour):
    pygame.draw.rect(gameDisplay, colour, [s_thingx, s_thingy, s_thingw, s_thingh])


def things(thingx, thingy, thingw, thingh, colour):                              # this function will define the obstacles to be avoided in the game
    pygame.draw.rect(gameDisplay, colour, [thingx, thingy, thingw, thingh])      # .draw lets us draw a rectangle (.rect), with a chosen colour and set of dimensions. the parameters of the location go in square brackets, thingx and thingy are the starting points and then thingw and thingh describe the full width and height of the object


def robo(x, y):
    gameDisplay.blit(ROBO_IMG, (x, y))                                           # .blit() is adding the chosen image to our window/surface at the location (x, y). (x, y) must be a separate tuple. (.blit() works in the background)


def text_objects(text, font):
    text_surface = font.render(text, True, drk_gry)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font("freesansbold.ttf", 100)                       # font.Font lets us define the font and its size
    TextSurf, TextRect = text_objects(text, large_text)                          # TextSurf tells the program to put the text in the window/surface. TextRect tells it to put the text in a rectangle so it can be positioned
    TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 4))                # centres the text using the rectangle TextRect
    gameDisplay.blit(TextSurf, TextRect)                                         # ".blit()"'s the rectangle with the text in to the surface

    pygame.display.update()                                                      # updates our display
    time.sleep(0.5)                                                                # puts the game to sleep for 2secs with the current display
    game_loop()                                                                  # restarts the game


def crash():
    message_display("OUT OF BOUNDS!!")


def impact():
    message_display("YOU'RE DEAD!!")


def intro_background(n, m):
    gameDisplay.blit(BACKGROUND_IMAGE, (n, m))


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    small_text = pygame.font.Font("freesansbold.ttf", 40)
    TextSurf, TextRect = text_objects(msg, small_text)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(TextSurf, TextRect)


def quit_game():
    pygame.quit()
    quit()


def game_intro():

    n = 0
    m = 0

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        intro_background(n, m)
        large_text = pygame.font.Font("freesansbold.ttf", 100)
        TextSurf, TextRect = text_objects("!ROBO DODGE!", large_text)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 4))
        gameDisplay.blit(TextSurf, TextRect)

        button("PLAY!", 350, 425, 250, 100, green, bright_green, game_loop)
        button("QUIT!", 655, 425, 250, 100, red, bright_red, quit_game)

        pygame.display.update()


def countdown():
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
            gameDisplay.fill(white)
            gameDisplay.blit(font.render(text, True, black), (350, 200))
            pygame.display.update()
            CLOCK.tick(60)
            continue


# def pause():
#
#
#
def scoreboard():

    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        large_text = pygame.font.Font("freesansbold.ttf", 100)
        TextSurf, TextRect = text_objects("PAUSED", large_text)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 4))
        gameDisplay.blit(TextSurf, TextRect)

        button("RESUME!", 350, 425, 250, 100, green, bright_green, game_loop)
        button("QUIT!", 655, 425, 250, 100, red, bright_red, quit_game)

        pygame.display.update()




def game_loop():                                                                 # defining a "game loop" gives the game better structure

    x = (DISPLAY_WIDTH * 0.40)
    y = (DISPLAY_HEIGHT * 0.75)

    s_thing_startx = random.randrange(0, DISPLAY_WIDTH)
    s_thing_starty = -400
    S_THING_SPEED = 4
    S_THING_WIDTH = 50
    S_THING_HEIGHT = 50

    thing_startx = random.randrange(0, DISPLAY_WIDTH)                            # these variables now create the dimensions of the obstacles we defined in the function things()
    thing_starty = -600
    THING_SPEED = 4
    THING_WIDTH = 200
    THING_HEIGHT = 200

    x_change = 0
    dodged = 0

    countdown()
    time.sleep(1)

    game_exit = False

    while not game_exit:                                                          # same as: while game_exit is still false

        for event in pygame.event.get():                                          # .get(() is a built-in function to "get" all the in-game events (clicking the mouse, pressing buttons etc)
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

        x += x_change                                                                        # this makes sure that x refreshes every time the robot moves
        gameDisplay.fill(white)                                                              # .fill() function lets us fill the background of the window/surface
        small_things(s_thing_startx, s_thing_starty, S_THING_WIDTH, S_THING_HEIGHT, blue)
        s_thing_starty += S_THING_SPEED
        things(thing_startx, thing_starty, THING_WIDTH, THING_HEIGHT, black)                 # function call to things() to place them into the game
        thing_starty += THING_SPEED                                                          # adding THING_SPEED to the starting point makes the object move, otherwise it would remain in the same place
        robo(x, y)                                                                           # calling the function robo(x, y) will ".blit()" our image
        things_dodged(dodged)

        if x > DISPLAY_WIDTH - ROBO_WIDTH or x < 0:                                          # Adds a boundary at the edge of the screen. DISPLAY_WIDTH - CAR_WIDTH is necessary because the x value starts in the top left hand corner of the image
            crash()

        if thing_starty > DISPLAY_HEIGHT:                                                    # this if statement checks to see if the obstacle has gone off the screen and if it has it generates a new object
            thing_starty = 0 - THING_HEIGHT
            thing_startx = random.randrange(0, DISPLAY_WIDTH)
            dodged += 1
            THING_SPEED += 0.5
            THING_WIDTH += (dodged * 1.2)

        if y < thing_starty + THING_HEIGHT:
            if x > thing_startx and \
               x < thing_startx + THING_WIDTH or \
               x + ROBO_WIDTH > thing_startx and \
               x + ROBO_WIDTH < thing_startx + THING_WIDTH:                                  # this series of comparisons checks to see if the obstacle is going to cross over the character and if it does then its displays the impact() message
                impact()

        if s_thing_starty > DISPLAY_HEIGHT:
            s_thing_starty = 0 - S_THING_HEIGHT
            s_thing_startx = random.randrange(0, DISPLAY_WIDTH)
            dodged += 1
            S_THING_SPEED += 0.8

        if y < s_thing_starty + S_THING_HEIGHT:
            if s_thing_startx < x and \
               s_thing_startx + S_THING_WIDTH > x or \
               s_thing_startx < x + ROBO_WIDTH and \
               s_thing_startx + S_THING_WIDTH > x + ROBO_WIDTH or \
               x < s_thing_startx and x + ROBO_WIDTH > s_thing_startx + S_THING_WIDTH:
                impact()

        pygame.display.update()                                                              # this will update the previous code so it can be displayed in the game window/surface (could also use .flip())
        CLOCK.tick(60)


game_intro()
pygame.quit()                                                                                # pygame must be un-initialised to quit
quit()
