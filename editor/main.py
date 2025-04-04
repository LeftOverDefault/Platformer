import json
import os
import pygame

import pygame._sdl2 as sdl2

from pygame._sdl2.window import Window


class Tileset:
    def __init__(self, index: int, path: str, tiles_x, tiles_y):
        self.index = index
        self.path = path
        self.image = pygame.image.load(path).convert_alpha()
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y

        self.tile_size = (self.image.get_width() // self.tiles_x, self.image.get_height() // self.tiles_y)

        self.tiles = self.split_tileset(self.image, self.tile_size, self.tiles_x, self.tiles_y)
    

    def has_pixels(self, sprite):
        # Get the surface of the sprite
        surface = sprite
        width, height = surface.get_size()
        
        # Iterate through each pixel
        for x in range(width):
            for y in range(height):
                if surface.get_at((x, y)) != (0, 0, 0, 0):  # Check if the pixel is not transparent
                    return True
        return False


    def __repr__(self):
        return self.image


    def split_tileset(self, tileset, tile_size: tuple[int, int], tiles_x, tiles_y) -> list[pygame.Surface]:
        tiles = []
        for y in range(tiles_y):
            for x in range(tiles_x):
                tile = pygame.Surface(tile_size, flags=pygame.SRCALPHA).convert_alpha()
                tile.blit(tileset, (-x * tile_size[0], -y * tile_size[1]))  #, (x * tile_size[0], 0))
                # if self.has_pixels(tile):
                tiles.append(tile)
        return tiles


class Button:
    def __init__(self, image: pygame.Surface, size: tuple[int, int], position: tuple[int, int], callback, *args):
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.size = size
        self.position = position
        self.callback = callback
        self.args = args

        self.pressed = False
    

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.position)


    def handle_input(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.callback(*self.args)
                self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.pressed = False


class Layer:
    def __init__(self, index: int):
        self.index = index
        self.name = f"Layer_{index + 1}"
        self.tiles = {}
    

    def rename(self, new_name: str) -> None:
        self.name = new_name


    def add_tile(self, tileset_index, tile_index, position: tuple[int, int]) -> None:
        self.tiles[f"{position[0]};{position[1]}"] = {
            "tile_index": tile_index,
            "tileset_index": tileset_index,
        }


    def draw(self, surface: pygame.Surface, tilesets: list[Tileset], camera: "Camera") -> None:
        for tile_index in self.tiles.keys():
            current_tile = self.tiles[tile_index]
            current_tileset = tilesets[current_tile["tileset_index"]]
            x = int(tile_index.split(";")[0]) * current_tileset.tile_size[0]
            y = int(tile_index.split(";")[1]) * current_tileset.tile_size[1]
            tile_pos: tuple[int, int] = (x + (pygame.display.get_surface().get_width() // 4) - camera.offset_x, y - camera.offset_y)
            surface.blit(current_tileset.tiles[current_tile["tile_index"]], tile_pos)


class Camera:
    def __init__(self):
        self.offset_x = ((pygame.display.get_surface().get_width() // 2) // 16) * 16
        self.offset_y = ((pygame.display.get_surface().get_height() // 2) // 16) * 16


    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.offset_y -= int(115 * dt)
        if keys[pygame.K_a]:
            self.offset_x -= int(115 * dt)
        if keys[pygame.K_s]:
            self.offset_y += int(115 * dt)
        if keys[pygame.K_d]:
            self.offset_x += int(115 * dt)


class Level:
    def __init__(self, font):
        self.name = "World 1"
        self.font = font
        self.active_tileset = 0
        self.active_tile = 0
        self.active_layer = 0
        self.layers: list[Layer] = []
        self.tilesets: list[Tileset] = []

        self.layer_names: list[pygame.Surface] = []

        self.active_tile_indicator = pygame.Surface((16 + 2, 16 + 2))
        self.active_tile_indicator.fill((255, 255, 255))
        self.active_tile_indicator_inner = pygame.Surface((16, 16))
        self.active_tile_indicator_inner.fill("#1B1E2B")


    def add_layer(self) -> None:
        self.layers.append(Layer(len(self.layers)))
        self.render_layer_names()
    

    def remove_layer(self) -> None:
        self.layers.pop(self.active_layer)
        self.render_layer_names()


    def add_tileset(self, path, tiles_x, tiles_y) -> None:
        self.tilesets.append(Tileset(len(self.tilesets), path, tiles_x, tiles_y))


    def render_layer_names(self) -> None:
        self.layer_names.clear()
        for layer in self.layers:
            color = (175, 175, 175)
            if layer.index == self.active_layer:
                color = (255, 255, 255)
            name_surface = self.font.render(layer.name, False, color, None, 0)
            self.layer_names.append(name_surface)


    def draw_layer_names(self, surface: pygame.Surface) -> None:
        for index, name_surface in enumerate(self.layer_names):
            surface.blit(name_surface, (5, 5 + (index * name_surface.get_height()) + (index * 2)))
    

    def draw_layers(self, surface: pygame.Surface, camera: Camera) -> None:
        for layer in self.layers:
            layer.draw(surface, self.tilesets, camera)
        

    def draw_tiles(self, surface: pygame.Surface) -> None:
        current_tileset = self.tilesets[self.active_tileset]
        for y in range(17):
            for x in range(8):
                tile_index = (y * 8) + x
                tile_size_x = current_tileset.tile_size[0]
                tile_size_y = current_tileset.tile_size[1]
                if tile_index == self.active_tile:
                    surface.blit(self.active_tile_indicator, ((x * tile_size_x) + (x * 2), (y * tile_size_y) + (y * 2)))
                    surface.blit(self.active_tile_indicator_inner, ((x * tile_size_x) + (x * 2) + 1, (y * tile_size_y) + (y * 2) + 1))
                surface.blit(current_tileset.tiles[tile_index], ((x * tile_size_x) + (x * 2) + 1, (y * tile_size_y) + (y * 2) + 1))


    def handle_events(self, event: pygame.Event, camera: Camera) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(self.layers) > 0:
                    relative_position = (event.pos[0] - (pygame.display.get_surface().get_width() // 4) + camera.offset_x, event.pos[1] + camera.offset_y)
                    tile_pos = [int(relative_position[0] // 16), int(relative_position[1] // 16)]
                    if f"{tile_pos[0]};{tile_pos[1]}" not in self.layers[self.active_layer].tiles.keys():
                        self.layers[self.active_layer].add_tile(self.active_tileset, self.active_tile, tile_pos)
            if event.button == 3:
                if len(self.layers) > 0:
                    relative_position = (event.pos[0] - (pygame.display.get_surface().get_width() // 4) + camera.offset_x, event.pos[1] + camera.offset_y)
                    tile_pos = [relative_position[0] // 16, relative_position[1] // 16]
                    if f"{tile_pos[0]};{tile_pos[1]}" in self.layers[self.active_layer].tiles.keys():
                        self.layers[self.active_layer].tiles.pop(f"{tile_pos[0]};{tile_pos[1]}")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                self.active_tile += 1 if self.active_tile < len(self.tilesets[self.active_tileset].tiles) else 0
            if event.key == pygame.K_PAGEUP:
                self.active_tile -= 1 if self.active_tile > 0 else 0
            if event.key == pygame.K_EQUALS:
                self.active_layer += 1 if self.active_layer < len(self.layers) - 1 else 0
                self.render_layer_names()
            if event.key == pygame.K_MINUS:
                self.active_layer -= 1 if self.active_layer > 0 else 0
                self.render_layer_names()
            if event.key == pygame.K_i:
                self.import_level()
            if event.key == pygame.K_e:
                self.export_level()


    def import_level(self) -> None:
        pass


    def export_level(self) -> None:
        data = {}

        data["name"] = self.name
        data["background"] = "#000000"

        data["tilesets"] = []
        data["layers"] = []
        data["entities"] = []
        data["objects"] = []

        for tileset in self.tilesets:
            data["tilesets"].append({
                "index": tileset.index,
                "image_path": tileset.path,
                "tile_width": tileset.tile_size[0],
                "tile_height": tileset.tile_size[1],
                "tiles_x": tileset.tiles_x,
                "tiles_y": tileset.tiles_y,
            })

        for layer in self.layers:
            data["layers"].append({
                "name": layer.name,
                "index": layer.index,
                "y_sorted": False,
                "collidable": False,
                "tiles": layer.tiles
            })
        

        with open(f"./out/{self.name.lower().replace(" ", "_")}.json", "w") as outfile_object:
            outfile_object.write(json.dumps(data))


class Editor:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.WIDTH = 192 * 3
        self.HEIGHT = 108 * 3

        self.SCALE_FACTOR = 2

        pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HIDDEN | pygame.SCALED, 0, 0, 0)
        
        # Set window properties
        self.window = sdl2.Window.from_display_module()
        self.window.size = (self.WIDTH * self.SCALE_FACTOR, self.HEIGHT * self.SCALE_FACTOR)
        self.window.position = sdl2.WINDOWPOS_CENTERED
        self.window.show()

        self.display_surface = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.fps: int = 60

        self.running = True
        self.fullscreen = False

        self.init()
    

    def init(self) -> None:
        self.font = pygame.font.Font("./assets/fonts/press_start.ttf", 8)

        self.sidenav = pygame.Surface((self.WIDTH // 4, self.HEIGHT))
        self.sidenav.fill("#1B1E2B")
        self.sidenav_rect = self.sidenav.get_rect(topleft=(0, 0))

        self.tile_view = pygame.Surface((self.WIDTH // 4, self.HEIGHT * (2 / 3)))
        self.tile_view.fill("#1B1E2B")
        self.tile_view_rect = self.tile_view.get_rect(topleft=(0, self.HEIGHT * (1 / 3)))

        self.canvas = pygame.Surface((self.WIDTH * (3 / 4), self.HEIGHT))
        self.canvas.fill((0, 0, 0))
        # self.canvas.fill("#292D3E")
        self.canvas_rect = self.canvas.get_rect(topleft=(self.WIDTH // 4, 0))

        self.origin_point = pygame.Surface((2, 2))
        self.origin_point.fill((255, 255, 255))
        self.origin_rect = self.origin_point.get_rect(center=(self.sidenav.get_width() + ((self.canvas.get_width() // 2) // 16) * 16, ((self.display_surface.get_height() // 2) // 16) * 16))

        self.level = Level(self.font)
        self.camera = Camera()

        self.level.add_tileset("./assets/sunny_land.png", 17, 8)

        add_image = pygame.image.load("./assets/add.png")
        minus_image = pygame.image.load("./assets/minus.png")
        self.add_layer_button = Button(add_image, (16, 16), (self.WIDTH // 4 - 16, 0), self.level.add_layer)
        self.minus_layer_button = Button(minus_image, (16, 16), (self.WIDTH // 4 - 16, 16), self.level.remove_layer)


    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.canvas, (self.WIDTH // 4, 0))
        self.level.draw_layers(surface, self.camera)
        surface.blit(self.origin_point, self.origin_rect)
        
        surface.blit(self.sidenav, self.sidenav_rect)
        self.level.draw_layer_names(surface)

        self.tile_view.fill("#1B1E2B")
        self.level.draw_tiles(self.tile_view)
        surface.blit(self.tile_view, self.tile_view_rect)

        self.add_layer_button.draw(surface)
        self.minus_layer_button.draw(surface)


    def update(self, dt: float) -> None:
        self.camera.update(dt)
        self.origin_rect.x = int((((self.sidenav.get_width() + (self.canvas.get_width() // 2) + (pygame.display.get_surface().get_width() // 2)) // 16) * 16) - self.camera.offset_x)
        self.origin_rect.y = int(((((self.canvas.get_height() // 16) * 16) - 1) - self.camera.offset_y))


    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        self.add_layer_button.handle_input(event)
        self.minus_layer_button.handle_input(event)
        self.level.handle_events(event, self.camera)


    def run(self) -> None:
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_events(event)
            
            dt = self.clock.tick(self.fps) / 1000

            self.render(self.display_surface)
            self.update(dt)

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    editor = Editor()
    editor.run()


# window_width = 192 * 3
# window_height = 108 * 3

# window_scale_factor = 2

# window = pygame.display.set_mode((window_width, window_height), pygame.HIDDEN | pygame.SCALED, 0, 0, 0)
# window = sdl2.Window.from_display_module()
# window.size = (window_width * window_scale_factor, window_height * window_scale_factor)
# window.position = sdl2.WINDOWPOS_CENTERED
# window.show()

# screen = pygame.display.get_surface()
# pygame.display.set_caption("Editor")

# clock = pygame.time.Clock()
# fps = 60

# tileset = pygame.image.load("./assets/sunny_land.png").convert_alpha()

# def split_tileset(tileset, tile_size: tuple[int, int], tiles_x, tiles_y) -> list[pygame.Surface]:
#     tiles = []
#     for y in range(tiles_y):
#         for x in range(tiles_x):
#             tile = pygame.Surface(tile_size, flags=pygame.SRCALPHA).convert_alpha()
#             tile.blit(tileset, (-x * tile_size[0], -y * tile_size[1]))  #, (x * tile_size[0], 0))
#             tiles.append(tile)
#     return tiles

# tiles = split_tileset(tileset, (16, 16), 17, 8)

# tiles_per_row = [1, 2, 4, 8, 17, 34, 68, 136][3]

# sidenav = pygame.Surface(((tiles_per_row * 16) + 18, window_height))
# sidenav.fill("#1b1e2b")

# active_tile = 0
# active_indicator = pygame.Surface((18, 18))
# active_indicator.fill((255, 255, 255))
# active_indicator_inner = pygame.Surface((16, 16))
# active_indicator_inner.fill("#1b1e2b")

# fullscreen = False
# running = True

# canvas = pygame.Surface((window_width - ((tiles_per_row * 16) + 18), window_height))


# canvas_offset: list[int, int] = [((-canvas.get_width() // 2) // 16) * 16, ((-canvas.get_height() // 2) // 16) * 16]

# canvas_origin = pygame.Surface((2, 2))
# canvas_origin.fill((255, 255, 255))

# layers = []

# painted_tiles = {}

# def render(surface: pygame.Surface):
#     canvas.fill("#292d3e")
#     sidenav.fill("#1b1e2b")

#     surface.blit(sidenav, (0, 0))
#     for y in range(int(len(tiles) / tiles_per_row)):
#         for x in range(tiles_per_row):
#             if y * tiles_per_row + x == active_tile:
#                 surface.blit(active_indicator, ((x * 16) + (x * 2) + 1, (y * 16) + (y * 2) + 1))
#                 surface.blit(active_indicator_inner, ((x * 16) + (x * 2) + 2, (y * 16) + (y * 2) + 2))
#             surface.blit(tiles[y * tiles_per_row + x], ((x * 16) + (x * 2) + 2, (y * 16) + (y * 2) + 2))
    
#     for tile_pos in painted_tiles.keys():
#         pos = tile_pos.split(";")
#         canvas.blit(painted_tiles[tile_pos], ((int(pos[0]) * 16) + canvas_offset[0], (int(pos[1]) * 16) + canvas_offset[1]))

#     canvas_origin.fill((255, 255, 255))

#     origin_position = (
#         ((((canvas.get_width() // 16) * 16) - 1) + canvas_offset[0]),
#         ((((canvas.get_height() // 16) * 16) - 1) + canvas_offset[1])
#     )

#     canvas.blit(canvas_origin, origin_position)

#     surface.blit(canvas, ((tiles_per_row * 16) + 18, 0))


# def update(dt: float):
#     keys = pygame.key.get_pressed()

#     if keys[pygame.K_w]:
#         canvas_offset[1] += int(130 * dt)
#     if keys[pygame.K_a]:
#         canvas_offset[0] += int(130 * dt)
#     if keys[pygame.K_s]:
#         canvas_offset[1] -= int(130 * dt)
#     if keys[pygame.K_d]:
#         canvas_offset[0] -= int(130 * dt)


# def event_handler(event: pygame.Event):
#     global active_tile
#     global fullscreen
#     global running
#     global window
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_PAGEDOWN:
#             active_tile += 1 if active_tile + 1 != len(tiles) else 0
#         if event.key == pygame.K_PAGEUP:
#             active_tile -= 1 if active_tile > 0 else 0
#         if event.key == pygame.K_F11:
#             fullscreen = not fullscreen
#             if fullscreen:
#                 window = pygame.display.set_mode((window_width, window_height), pygame.SCALED | pygame.FULLSCREEN, 0, 0, 0)
#             else:
#                 window = pygame.display.set_mode((window_width, window_height), pygame.SCALED, 0, 0, 0)
#         if event.key == pygame.K_ESCAPE:
#             running = False
#     if event.type == pygame.MOUSEBUTTONDOWN:
#         if event.button == 1:
#             relative_event_pos: tuple[int, int] = (event.pos[0] - sidenav.get_width() - canvas_offset[0], event.pos[1] - canvas_offset[1])
#             tile_pos = [relative_event_pos[0] // 16, relative_event_pos[1] // 16]
#             if f"{tile_pos[0]};{tile_pos[1]}" not in painted_tiles.keys():
#                 painted_tiles[f"{tile_pos[0]};{tile_pos[1]}"] = tiles[active_tile]
#         if event.button == 3:
#             relative_event_pos: tuple[int, int] = (event.pos[0] - sidenav.get_width() - canvas_offset[0], event.pos[1] - canvas_offset[1])
#             tile_pos = [relative_event_pos[0] // 16, relative_event_pos[1] // 16]
#             if f"{tile_pos[0]};{tile_pos[1]}" in painted_tiles.keys():
#                 painted_tiles.pop(f"{tile_pos[0]};{tile_pos[1]}")


# def main():
#     global running
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             event_handler(event)

#         dt = clock.tick(fps) / 1000

#         screen.fill((0, 0, 0))

#         render(screen)
#         update(dt)
        
#         pygame.display.update()


# if __name__ == "__main__":
#     main()
