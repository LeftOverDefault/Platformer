from world_engine.utils.imports import *


class CanvasTile(pygame.sprite.Sprite):
    def __init__(self, image, tile_index, position, group) -> None:
        super().__init__(group)
        self.image = image
        self.tile_index = tile_index
        self.rect = self.image.get_rect(topleft=position)
