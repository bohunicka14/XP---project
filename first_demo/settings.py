import pygame
pygame.init()

# game options/settings
TITLE = "Super Space Cpt Dankis"
WIDTH = 1280
HEIGHT = 600
FPS = 60
SPRITESHEET_PLAYER = "IMAGES/p1_spritesheet.png"
SPRITESHEET_ENEMY = "IMAGES/enemies_spritesheet.png"
SPRITESHEET_OTHER = "IMAGES/spritesheet_jumper.png"
HS_FILE = "highscore.txt"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25

# Enemy properties


# Game properties
TREAT_SPAWN = 7

# Starting platforms
PLATFORM_LIST_LEVEL_1 = [(0, HEIGHT - 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100),
                 (275, 100),
                 (375, 100),
                 (475, 100),
                 (575, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)

BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
