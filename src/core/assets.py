import pygame

from utilities.sprite import slice_sheet


# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load( "assets/textures/icons/icon.png" )

TILESET = slice_sheet( "assets/textures/tilesets/sunny_land.png", 16, 16 )

SUNNY_LAND_0 = pygame.image.load("assets/textures/background/sunny_land/0.png")
SUNNY_LAND_1 = pygame.image.load("assets/textures/background/sunny_land/1.png")
# SUNNY_ROCKY_2 = pygame.image.load("assets/textures/background/sunny_rocky/2.png")
# SUNNY_ROCKY_3 = pygame.image.load("assets/textures/background/sunny_rocky/3.png")

# Load audio (ogg for web compatibility)
# DEBUG_THEME = pygame.mixer.Sound( "assets/sound/platformer_level03_loop.ogg" )

# Load fonts (ttf for web compatibility)
DEBUG_FONT = pygame.font.Font( "assets/font/joystix.ttf", 10 )

print( "Loaded assets" )
