import pygame
from enum import IntEnum, auto


class InputState( IntEnum ):
    NOTHING = 0
    PRESSED = auto()
    HELD = auto()
    RELEASED = auto()


class MouseButton( IntEnum ):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class Action( IntEnum ):
    LEFT = 0
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    A = auto()
    B = auto()
    SELECT = auto()
    START = auto()
    DEBUG = auto()


action_mappings = {
    Action.LEFT: [ pygame.K_a, pygame.K_LEFT ],
    Action.RIGHT: [ pygame.K_d, pygame.K_RIGHT ],
    Action.UP: [ pygame.K_w, pygame.K_UP ],
    Action.DOWN: [ pygame.K_s, pygame.K_DOWN ],
    Action.A: [ pygame.K_z, pygame.K_SLASH ],
    Action.B: [ pygame.K_x, pygame.K_PERIOD ],
    Action.SELECT: [ pygame.K_LSHIFT, pygame.K_RSHIFT ],
    Action.START: [ pygame.K_RETURN, pygame.K_SPACE ],
    Action.DEBUG: [ pygame.K_NUMLOCK, pygame.K_BACKQUOTE ]
}


InputBuffer = list[ InputState ]
