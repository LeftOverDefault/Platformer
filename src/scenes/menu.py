import pygame
import sys

import core.constants as const
import core.input as input
import core.assets as assets
from components.animation import AnimationPlayer

from scenes.scene import Scene

from ui.button import Button

class Menu(Scene):
    def __init__(self, statemachine):
        super().__init__(statemachine)

        self.button = Button((100, 100), (200, 50), "Play", (255, 255, 255), (0, 0, 0), lambda: print("Hello, World!"))

    def enter(self) -> None:
        ...

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: input.InputBuffer,
        mouse_buffer: input.InputBuffer
    ) -> None:
        if (
            action_buffer[input.Action.START] == input.InputState.PRESSED or
            mouse_buffer[input.MouseButton.LEFT] == input.InputState.PRESSED
        ):
            self.button.handle_button_down()
            # self.statemachine.change_state(scenes.examples.game.Game)
            return
        elif (
            action_buffer[input.Action.START] == input.InputState.RELEASED or
            mouse_buffer[input.MouseButton.LEFT] == input.InputState.RELEASED
        ):
            return
        elif (
            action_buffer[input.Action.START] == input.InputState.HELD or
            mouse_buffer[input.MouseButton.LEFT] == input.InputState.HELD
        ):
            self.button.handle_button_up()
            return


        # DEBUG.update(dt)

        surface.fill(const.CYAN)

        self.button.draw(surface)
        # surface.blit(DEBUG.get_frame(), (DEBUG_X, DEBUG_Y))

    def exit(self) -> None:
        pass

