import pygame


# def draw_bg( surface: pygame.Surface, background: pygame.Surface, scroll: float, depth: float, y: float, y_offset):
#     # If the background is placed far away -- by the rules of perspective,
#     # the change of position in XY would be smaller by 1/Z.
#     x = scroll / depth
#     y /= (depth * 4)

#     # X should loop back when it's out of range of the background's size.
#     x %= background.get_width()

#     # We want to be as efficient with our calls as possible.
#     # If `x` is not out of the window, we can draw the main piece of the background.
#     if x <= surface.get_width():
#         surface.blit( background, ( x, y + y_offset ) )

#     # If `x + background.get_width()` is not out of the window, we need to draw another piece of background.
#     if x + (background.get_width()) <= surface.get_width():
#         surface.blit( background, ( x + background.get_width(), y + y_offset ) )

#     # We need the background to loop; it happens that the back part gets left out.
#     # Unless the main piece had covered it (x == 0), we'll draw it behind the main piece.
#     if x != 0:
#         surface.blit( background, ( x - background.get_width(), y + y_offset ) )


def draw_bg(surface: pygame.Surface, background: pygame.Surface, scroll: float, depth: float, y: float, y_offset: float):
    # Adjust x and y based on depth for parallax effect
    x = scroll / depth
    y /= (depth * 4)

    # Ensure x wraps around properly
    bg_width = background.get_width()
    x %= bg_width

    # Number of images needed to fully cover the screen width
    num_tiles = (surface.get_width() // bg_width) + 2  # +2 ensures coverage even with offsets

    # Draw enough background images to fill the screen
    for i in range(num_tiles):
        surface.blit(background, (x + i * bg_width - bg_width, y + y_offset))
