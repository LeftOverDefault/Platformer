from world_engine.classes.layer import Layer
from world_engine.classes.tile.canvas_tile import CanvasTile
from world_engine.func.import_cut_graphics import import_cut_graphics
from world_engine.utils.imports import *


class Canvas:
    def __init__(self, display_surface, camera, config) -> None:
        self.display_surface = display_surface
        self.config = config
        self.camera = camera

        self.tileset = import_cut_graphics(self.config.tilesets[self.config.current_tileset], self.config)
        self.sidenav_width = (pygame.display.get_surface().get_width() / self.config.screen_multiplier) * (3 / 2)

        self.layers = []

        self.create_layers()


    def create_layers(self):
        for layer in self.config.layers:
            self.layers.append(Layer())


    def create_tile(self, current_tile_index, current_layer_index) -> None:
        current_layer = self.layers[current_layer_index]
        if pygame.mouse.get_pos()[0] > self.sidenav_width:
            current_x = int(int((pygame.mouse.get_pos()[0] / ((pygame.display.get_surface().get_width() / 198) / self.config.display_surface_multiplier)) + self.camera.offset.x) // self.config.tile_size) * self.config.tile_size
            current_y = int(int((pygame.mouse.get_pos()[1] / ((pygame.display.get_surface().get_height() / 108) / self.config.display_surface_multiplier)) + self.camera.offset.y) // self.config.tile_size) * self.config.tile_size

            if pygame.mouse.get_pressed()[0]:
                tile_pos = [current_x // self.config.tile_size, current_y // self.config.tile_size]
                tile_location = [current_x, current_y]
                if tile_pos not in current_layer.tile_positions:
                    current_layer.tile_positions.append(tile_pos)
                    CanvasTile(self.tileset[current_tile_index], current_tile_index, tile_location, current_layer)

            if pygame.mouse.get_pressed()[2]:
                for sprite in current_layer:
                    if sprite.rect.x == current_x and sprite.rect.y == current_y:
                        current_layer.remove(sprite)
                        current_layer.tile_positions.remove([current_x // self.config.tile_size, current_y // self.config.tile_size])
    

    def draw_tiles(self) -> None:
        self.camera.empty()
        for layer in self.layers:
            for tile in layer:
                self.camera.add(tile)
