import pygame


class View:
    def __init__(self, x, y, width, height, anchor='center'):
        self.rect = pygame.Rect(x, y, width, height)
        self.anchor = anchor  # Anchor point (e.g., center, top-left, etc.)
        self.children = []
        self.resizing = False  # State to track resizing
        self.resize_edge = None  # To store which edge/corner is being dragged
        self.min_size = (50, 50)  # Minimum allowed size for the view

    def add_child(self, child, offset=(0, 0)):
        """Add a GUI element (Button, InputBox, etc.) to this view with a specific offset."""
        child.offset = offset  # Set the offset for the child
        self.children.append(child)
        self.reposition_children()

    def remove_child(self, child):
        """Remove a GUI element."""
        self.children.remove(child)

    def resize(self, width, height):
        """Resize the view and update the position of all child elements."""
        self.rect.width = max(width, self.min_size[0])  # Ensure minimum width
        self.rect.height = max(height, self.min_size[1])  # Ensure minimum height
        self.reposition_children()

    def reposition_children(self):
        """Reposition children elements according to the current view's size and anchor."""
        for child in self.children:
            child.reposition(self.rect)

    def draw(self, surface):
        """Draw the view and its children on the given surface."""
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # Draw border for the view
        for child in self.children:
            child.draw(surface)

    def handle_event(self, event):
        """Handle mouse and other events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.resizing = True
                self.resize_edge = self._get_resize_edge(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.resizing:
                self._resize_view(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.resizing = False
            self.resize_edge = None

    def _get_resize_edge(self, mouse_pos):
        """Determine which edge or corner is being clicked for resizing."""
        x, y = mouse_pos
        edge_margin = 10  # Area near edges/corners to trigger resizing
        
        # Check corners first
        if self.rect.collidepoint(x, y):
            if (x > self.rect.right - edge_margin and y > self.rect.bottom - edge_margin):
                return 'bottom-right'
            elif (x < self.rect.left + edge_margin and y > self.rect.bottom - edge_margin):
                return 'bottom-left'
            elif (x > self.rect.right - edge_margin and y < self.rect.top + edge_margin):
                return 'top-right'
            elif (x < self.rect.left + edge_margin and y < self.rect.top + edge_margin):
                return 'top-left'
            # Check sides
            elif x < self.rect.left + edge_margin:
                return 'left'
            elif x > self.rect.right - edge_margin:
                return 'right'
            elif y < self.rect.top + edge_margin:
                return 'top'
            elif y > self.rect.bottom - edge_margin:
                return 'bottom'
        return None

    def _resize_view(self, mouse_pos):
        """Resize the view based on the mouse position."""
        x, y = mouse_pos
        if self.resize_edge == 'top-left':
            self.resize(x, self.rect.bottom - y)
            self.rect.left = x
        elif self.resize_edge == 'top-right':
            self.resize(self.rect.right - x, self.rect.bottom - y)
            self.rect.right = x
        elif self.resize_edge == 'bottom-left':
            self.resize(x - self.rect.left, y - self.rect.top)
            self.rect.left = x
        elif self.resize_edge == 'bottom-right':
            self.resize(x - self.rect.left, y - self.rect.top)
        elif self.resize_edge == 'top':
            self.resize(self.rect.width, self.rect.bottom - y)
            self.rect.top = y
        elif self.resize_edge == 'bottom':
            self.resize(self.rect.width, y - self.rect.top)
        elif self.resize_edge == 'left':
            self.resize(x - self.rect.left, self.rect.height)
            self.rect.left = x
        elif self.resize_edge == 'right':
            self.resize(x - self.rect.left, self.rect.height)

class GUIElement:
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
