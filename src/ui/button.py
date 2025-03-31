import pygame

from typing import Tuple, Union


class Button:
    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        text: str,
        text_color: Union[str, Tuple[int, int, int]],
        bg_color: Union[str, Tuple[int, int, int]],
        method: callable = lambda: None,
    ) -> None:
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.SysFont("Arial", size[1])
        self.text_surf = self.font.render(text, False, text_color)

        self.color = bg_color
        self.text = text
        self.func = method

        self._text_pos = self.text_surf.get_rect(center=self.rect.center).topleft

        self._is_pressed = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the pygame.Rect and font"""
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(
            self.text_surf,
            self._text_pos,
        )

    def handle_button_down(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self._is_pressed = True
            self.func()
    
    def handle_button_up(self) -> None:
        self._is_pressed = False

