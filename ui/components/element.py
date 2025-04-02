import pygame


class Element:
    """Base class for any GUI element (Button, InputBox, etc.)"""
    def __init__(self, x, y, width, height, anchor='center'):
        self.rect = pygame.Rect(x, y, width, height)
        self.anchor = anchor
        self.offset = (0, 0)  # Offset from parent view's origin

    def reposition(self, parent_rect):
        """Reposition the element inside the parent container with an offset."""
        x, y = self.offset
        # Add offset to the element's position inside the parent view
        if self.anchor == 'center':
            self.rect.center = parent_rect.center
        elif self.anchor == 'top-left':
            self.rect.topleft = parent_rect.topleft
        elif self.anchor == 'top-right':
            self.rect.topright = parent_rect.topright
        elif self.anchor == 'bottom-left':
            self.rect.bottomleft = parent_rect.bottomleft
        elif self.anchor == 'bottom-right':
            self.rect.bottomright = parent_rect.bottomright
        # You can add more anchor types if needed

        # Adjust for the offset relative to the parent
        self.rect.x += x
        self.rect.y += y

    def draw(self, surface):
        """Draw the GUI element on the screen."""
        raise NotImplementedError("This method should be implemented by subclasses.")
