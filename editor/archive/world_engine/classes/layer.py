from world_engine.utils.imports import *


class Layer(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.tile_positions = []
