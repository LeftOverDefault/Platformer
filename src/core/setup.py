import sys
import platform
import pygame
import pygame._sdl2 as sdl2

import core.constants as const


pygame.init()

if sys.platform == "emscripten":  # If running in browser
    platform.window.canvas.style.imageRendering = "pixelated"
    window = pygame.display.set_mode( const.WINDOW_SETUP["size"] )
else:
    window = pygame.display.set_mode( **const.WINDOW_SETUP )

initial_scale_factor = 2  # <-- adjustable
window = sdl2.Window.from_display_module()
window.size = (const.WINDOW_WIDTH * initial_scale_factor, const.WINDOW_HEIGHT * initial_scale_factor)
window.position = sdl2.WINDOWPOS_CENTERED
window.show()

clock = pygame.time.Clock()

print( "Setup complete" )
