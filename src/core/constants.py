import pygame


# Pygame constants
WINDOW_SCALE_FACTOR = 2

WINDOW_WIDTH = int(192 * WINDOW_SCALE_FACTOR)
WINDOW_HEIGHT = int(108 * WINDOW_SCALE_FACTOR)
WINDOW_SIZE = ( WINDOW_WIDTH, WINDOW_HEIGHT )
WINDOW_CENTRE = ( WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 )

WINDOW_SETUP = {
    "size": WINDOW_SIZE,
    "flags": pygame.SCALED | pygame.HIDDEN, # | pygame.FULLSCREEN,
    "depth": 0,
    "display": 0,
    "vsync": 0,
}

CAPTION = "Platformer"
FPS = 60  # 0 = Uncapped -> let VSYNC decide best tick speed if enabled
MAX_DT = 1 / 60

# Colour constants
WHITE = pygame.Color( 255, 255, 255 )
BLACK = pygame.Color( 0, 0, 0 )
RED = pygame.Color( 255, 0, 0 )
YELLOW = pygame.Color( 255, 255, 0 )
GREEN = pygame.Color( 0, 255, 0 )
CYAN = pygame.Color( 0, 255, 255 )
BLUE = pygame.Color( 0, 0, 255 )
MAGENTA = pygame.Color( 255, 0, 255 )

# BACKGROUND = "#3C65FF"
BACKGROUND = "#325762"

print( "Loaded constants" )
