from world_engine.utils.imports import *


def import_cut_graphics(path, config) -> list:
    cut_tiles = []

    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / config.tile_size)
    tile_num_y = int(surface.get_size()[1] / config.tile_size)

    for row in range(tile_num_y):
        for column in range(tile_num_x):
            x = column * config.tile_size
            y = row * config.tile_size
            new_surface = pygame.Surface(size=(config.tile_size, config.tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(source=surface, dest=(0, 0), area=pygame.Rect(x, y, config.tile_size, config.tile_size))
            cut_tiles.append(new_surface)
    
    return cut_tiles
