from world_engine.utils.imports import *


class LetterTile(pygame.sprite.Sprite):
    def __init__(self, image, index, position, group) -> None:
        super().__init__(group)
        self.image = image
        self.index = index
        self.rect = self.image.get_rect(topleft=position)
