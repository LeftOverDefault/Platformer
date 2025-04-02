import pygame

from components.element import Element


class InputBox(Element):
    def __init__(self, x, y, width, height, font, anchor='center', offset=(0, 0)):
        super().__init__(x, y, width, height, anchor)
        self.font = font
        self.text = ""
        self.active = False
        self.color = (255, 255, 255)  # Background color
        self.border_color = (0, 0, 0)  # Border color
        self.offset = offset  # Store offset

    def draw(self, surface):
        # Draw the input box background and border
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        # Draw the text inside the input box
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, self.rect.topleft)

    def handle_event(self, event):
        """Handle user input (keyboard events)."""
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
