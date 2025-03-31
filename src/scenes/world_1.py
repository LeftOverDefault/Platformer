import pygame
import time
import math

import core.constants as const
import core.input as input
import core.assets as assets
from components.animation import AnimationPlayer
from utilities.draw_bg import draw_bg

from scenes.scene import Scene

from components.ui.button import Button


class World1( Scene ):
    def __init__( self, statemachine ):
        super().__init__( statemachine )

        self.button = Button( ( 100, 100 ), ( 200, 50 ), "Play", ( 255, 255, 255 ), ( 0, 0, 0 ), lambda: print( "Hello, World!" ) )

        self.fade_surf = pygame.Surface(pygame.display.get_surface().get_size())
        self.fade_surf_color = pygame.Color(0, 0, 0)
        self.fade_surf_alpha = 255

        self.y = 0
        self.bg_scroll = 0


    def enter(self) -> None:
        ...


    def update(self, delta_time: float) -> None:
        if self.fade_surf_color.a > 0:
            self.fade_surf_alpha -= 2
        
        self.fade_surf.set_alpha(self.fade_surf_alpha)

        self.y = 0
        # y = -500 * math.sin(time.perf_counter())
        self.bg_scroll = 500 * math.sin(time.perf_counter())
        # bg_scroll = -500 * time.perf_counter()


    def render(self, surface: pygame.Surface) -> None:
        surface.fill( const.BACKGROUND )

        # Draw the backgrounds in order from the furthest to the nearest.
        draw_bg(surface, assets.SUNNY_ROCK_0, self.bg_scroll, 50, 0, 0)
        draw_bg(surface, assets.SUNNY_ROCK_1, self.bg_scroll, 20, self.y, 30)
        draw_bg(surface, assets.SUNNY_ROCK_2, self.bg_scroll, 10, self.y, 70)

        surface.blit(self.fade_surf)


    def execute( self, surface: pygame.Surface, dt: float, action_buffer: input.InputBuffer, mouse_buffer: input.InputBuffer ) -> None:
        if ( action_buffer[ input.Action.START ] == input.InputState.HELD or mouse_buffer[ input.MouseButton.LEFT ] == input.InputState.HELD ):
            self.button.handle_button_held()
            # self.statemachine.change_state(scenes.examples.game.Game)
            return
        elif ( action_buffer[ input.Action.START ] == input.InputState.PRESSED or mouse_buffer[ input.MouseButton.LEFT ] == input.InputState.PRESSED ):
            self.button.handle_button_down()
            # self.statemachine.change_state(scenes.examples.game.Game)
            return
        elif ( action_buffer[ input.Action.START ] == input.InputState.HELD or mouse_buffer[ input.MouseButton.LEFT ] == input.InputState.HELD ):
            self.button.handle_button_up()
            return

        self.update(dt)
        self.render(surface)


    def exit(self) -> None:
        ...

