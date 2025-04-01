import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x, y, collideable=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collideable = collideable
    

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


class PlatformTile(Tile):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
