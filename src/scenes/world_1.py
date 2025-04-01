import pygame
import time
import math

from components.animation import AnimationPlayer
from components.player import Player
from components.ui.button import Button

import core.constants as const
import core.input as input
import core.assets as assets

from scenes.scene import Scene

from utilities.draw_bg import draw_bg
from utilities.sprite import get_sprite_from_sheet


class World1( Scene ):
    def __init__( self, statemachine ):
        super().__init__( statemachine )

        # self.player = Player((0, 0), [], [])

        # get_sprite_from_sheet(assets.TILESET, 0, 0, 16, 16)

        # self.player = pygame.Surface((16, 16))
        # self.player.fill((255, 0, 0))
        # self.player_rect = self.player.get_rect(topleft = (58, 32))

        # self.sprite.fill("red")

        self.fade_surf = pygame.Surface(pygame.display.get_surface().get_size())
        self.fade_surf_color = pygame.Color(0, 0, 0)
        self.fade_surf_alpha = 255

        # self.y = 0
        # self.bg_scroll = 0
        # self.sky_scroll = 0


    def enter(self) -> None:
        ...


    def update(self, dt: float) -> None:
        if self.fade_surf_color.a > 0:
            self.fade_surf_alpha -= 2

        self.fade_surf.set_alpha(self.fade_surf_alpha)

        # self.y = 0 * dt
        # self.bg_scroll = 0 * dt
        # self.sky_scroll = self.bg_scroll * dt
        # self.y = -500 * math.sin(time.perf_counter())  # * dt
        # self.bg_scroll = 1000 * math.sin(time.perf_counter())  # * dt
        # self.sky_scroll = 5 * time.perf_counter()  # * dt


    def render(self, surface: pygame.Surface) -> None:
        surface.fill( const.BACKGROUND )

        # Draw the backgrounds in order from the furthest to the nearest.
        # draw_bg(surface, assets.SUNNY_LAND_0, self.sky_scroll, 100, 0, 0)
        # draw_bg(surface, assets.SUNNY_LAND_1, self.bg_scroll, 50, self.y, 120)

        # x = 0
        # y = 0
        # for i in range(len(assets.TILESET)):
        # # for y in range(0, 5):
        # #     for x in range(0, 5):
        #     surface.blit(assets.TILESET[i], (58 + (x * 16), 48 + (y * 16)))
        #     x += 1
        #     if x == 17:
        #         y += 1
        #         x = 0
        
        # surface.blit(self.player, self.player_rect)

        surface.blit(self.fade_surf)


    def execute( self, surface: pygame.Surface, dt: float, action_buffer: input.InputBuffer, mouse_buffer: input.InputBuffer ) -> None:
        if ( action_buffer[ input.Action.START ] == input.InputState.HELD or mouse_buffer[ input.MouseButton.LEFT ] == input.InputState.HELD ):
            # self.button.handle_button_held()
            # self.statemachine.change_state(scenes.examples.game.Game)
            return
        elif ( action_buffer[ input.Action.START ] == input.InputState.PRESSED or mouse_buffer[ input.MouseButton.LEFT ] == input.InputState.PRESSED ):
            # self.button.handle_button_down()
            # self.statemachine.change_state(scenes.examples.game.Game)
            return
        elif ( action_buffer[ input.Action.START ] == input.InputState.HELD or mouse_buffer[ input.MouseButton.LEFT ] == input.InputState.HELD ):
            # self.button.handle_button_up()
            return

        self.update(dt)
        self.render(surface)


    def exit(self) -> None:
        ...

