from world_engine.classes.tile.letter_tile import LetterTile
from world_engine.classes.tile.sidenav_tile import SidenavTile
from world_engine.font.font import Font
from world_engine.func.array_split import array_split
from world_engine.func.import_cut_graphics import import_cut_graphics
from world_engine.utils.imports import *


class Sidenav:
    def __init__(self, display_surface, config) -> None:
        self.display_surface = display_surface
        self.config = config

        self.tile_group = pygame.sprite.Group()
        self.layer_group = pygame.sprite.Group()

        self.font = Font(self.config.font, self.config.font_size, self.config.font_colour, config=self.config)

        self.scroll_height = 0
        self.current_tile = 0
        self.current_layer = 0

        self.tiles_per_row = 5
        self.tiles = list(array_split(import_cut_graphics(self.config.tilesets[self.config.current_tileset], self.config), self.tiles_per_row)) # list(self.original_tiles.keys()), len(list(self.original_tiles.keys())) // self.tiles_per_row))

        self.sidenav_surface = pygame.Surface((198 / 2, self.display_surface.get_height()))
        self.layer_surface = pygame.Surface(((198 / 2) - 2, self.display_surface.get_height() * (1 / 3) - 1))
        self.tile_surface = pygame.Surface(((198 / 2) - 2, (len(self.tiles) + self.tiles_per_row) * self.config.tile_size))

        self.draw_tiles()
        self.draw_layers()

        self.tile_mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        self.layer_mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)


    def draw_tiles(self) -> None:
        for y, tile_array in enumerate(self.tiles):
            for x, tile in enumerate(tile_array):
                tile_index = ((y * self.tiles_per_row) + x)
                SidenavTile(tile, tile_index, (x * (self.config.tile_size + 2), y * (self.config.tile_size + 2)), self.tile_group)
    

    def draw_layers(self) -> None:
        for layer_index, layer in enumerate(self.config.layers):
            images = self.font.return_image(layer)
            for image_array in images:
                image = image_array[0]
                x_position = image_array[1]
                LetterTile(image, layer_index, (x_position + self.font.space_width, (layer_index * self.font.line_height) + self.font.space_width), self.layer_group)


    def scroll(self, event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            if ((len(self.tiles) + self.tiles_per_row) * -self.config.tile_size) + (self.display_surface.get_height() * (2 / 3)) <= self.scroll_height + (event.y * 8) <= 0:
                self.scroll_height += event.y * 8


    def get_current_tile(self) -> None:
        self.tile_mouse_rect.x = pygame.mouse.get_pos()[0] / (self.config.screen_multiplier / self.config.display_surface_multiplier)
        self.tile_mouse_rect.y = (pygame.mouse.get_pos()[1] / (self.config.screen_multiplier / self.config.display_surface_multiplier)) - (self.scroll_height + self.layer_surface.get_height())
        if pygame.mouse.get_pos()[1] // (self.config.screen_multiplier / self.config.display_surface_multiplier) > self.display_surface.get_height() * (1 / 3):
            for tile in self.tile_group:
                if self.tile_mouse_rect.colliderect(tile.rect):
                    if pygame.mouse.get_pressed()[0]:
                        self.current_tile = tile.tile_index
    

    def get_current_layer(self) -> None:
        self.layer_mouse_rect.x = pygame.mouse.get_pos()[0] // (self.config.screen_multiplier // self.config.display_surface_multiplier)
        self.layer_mouse_rect.y = (pygame.mouse.get_pos()[1] // (self.config.screen_multiplier // self.config.display_surface_multiplier))
        if pygame.mouse.get_pressed()[0]:
            if self.layer_mouse_rect.x <= self.layer_surface.get_width():
                if pygame.mouse.get_pos()[1] // (self.config.screen_multiplier // self.config.display_surface_multiplier) < self.display_surface.get_height() * (1 / 3):
                    for layer_index in range(len(self.config.layers)):
                        if int(self.layer_mouse_rect.y) in range((layer_index * self.font.line_height), ((layer_index + 1) * self.font.line_height)):
                            self.current_layer = layer_index


    def draw(self) -> None:
        self.sidenav_surface.fill("#11131b")
        self.tile_surface.fill("#1b1e2b")
        self.layer_surface.fill("#1b1e2b")

        self.tile_group.draw(self.tile_surface)

        self.layer_group.draw(self.layer_surface)

        self.sidenav_surface.blit(self.tile_surface, (1, self.display_surface.get_height() * (1 / 3) + self.scroll_height))
        self.sidenav_surface.blit(self.layer_surface, (1, 0))

        pygame.draw.line(self.sidenav_surface, "#11131b", (0, self.layer_surface.get_height()), (self.sidenav_surface.get_width(), self.layer_surface.get_height()))

        self.display_surface.blit(self.sidenav_surface, (0, 0))
