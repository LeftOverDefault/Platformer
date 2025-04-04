import pygame

from components.element import Element


class Button(Element):
    def __init__(self, x, y, width, height, text, font, anchor='center', offset=(0, 0)):
        super().__init__(x, y, width, height, anchor)
        self.text = text
        self.font = font
        self.color = (200, 200, 200)  # Default button color
        self.text_color = (0, 0, 0)   # Text color
        self.offset = offset  # Store offset

    def draw(self, surface):
        # Draw the button background
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw the text in the center of the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_pressed(self, mouse_pos):
        """Check if the button is pressed."""
        return self.rect.collidepoint(mouse_pos)
