import pygame

from utilities.sprite import slice_sheet


# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load( "assets/textures/icons/icon.png" )

SUNNY_ROCK_0 = pygame.image.load("assets/textures/parallax/sunny_rock/0.png")
SUNNY_ROCK_1 = pygame.image.load("assets/textures/parallax/sunny_rock/1.png")
SUNNY_ROCK_2 = pygame.image.load("assets/textures/parallax/sunny_rock/2.png")
SUNNY_ROCK_3 = pygame.image.load("assets/textures/parallax/sunny_rock/3.png")

# Load audio (ogg for web compatibility)
# DEBUG_THEME = pygame.mixer.Sound( "assets/sound/platformer_level03_loop.ogg" )

# Load fonts (ttf for web compatibility)
DEBUG_FONT = pygame.font.Font( "assets/font/joystix.ttf", 10 )

print( "Loaded assets" )
