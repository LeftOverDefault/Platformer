import pygame
import pygame._sdl2 as sdl2


window_width = 192 * 3
window_height = 108 * 3

window_scale_factor = 2

window = pygame.display.set_mode((window_width, window_height), pygame.HIDDEN | pygame.SCALED, 0, 0, 0)
window = sdl2.Window.from_display_module()
window.size = (window_width * window_scale_factor, window_height * window_scale_factor)
window.position = sdl2.WINDOWPOS_CENTERED
window.show()

screen = pygame.display.get_surface()
pygame.display.set_caption("Editor")

clock = pygame.time.Clock()
fps = 60

tileset = pygame.image.load("./assets/sunny_land.png").convert_alpha()

def split_tileset(tileset, tile_size: tuple[int, int], tiles_x, tiles_y) -> list[pygame.Surface]:
    tiles = []
    for y in range(tiles_y):
        for x in range(tiles_x):
            tile = pygame.Surface(tile_size, flags=pygame.SRCALPHA).convert_alpha()
            tile.blit(tileset, (-x * tile_size[0], -y * tile_size[1]))  #, (x * tile_size[0], 0))
            tiles.append(tile)
    return tiles

tiles = split_tileset(tileset, (16, 16), 17, 8)

tiles_per_row = [1, 2, 4, 8, 17, 34, 68, 136][3]

sidenav = pygame.Surface(((tiles_per_row * 16) + 18, window_height))
sidenav.fill("#1b1e2b")

active_tile = 0
active_indicator = pygame.Surface((18, 18))
active_indicator.fill((255, 255, 255))
active_indicator_inner = pygame.Surface((16, 16))
active_indicator_inner.fill("#1b1e2b")

fullscreen = False
running = True

canvas = pygame.Surface((window_width - ((tiles_per_row * 16) + 18), window_height))

canvas_offset: list[int, int] = [((-canvas.get_width() // 2) // 16) * 16, ((-canvas.get_height() // 2) // 16) * 16]

canvas_origin = pygame.Surface((2, 2))
canvas_origin.fill((255, 255, 255))

layers = []

painted_tiles = {}

def render(surface: pygame.Surface):
    canvas.fill("#292d3e")
    sidenav.fill("#1b1e2b")

    surface.blit(sidenav, (0, 0))
    for y in range(int(len(tiles) / tiles_per_row)):
        for x in range(tiles_per_row):
            if y * tiles_per_row + x == active_tile:
                surface.blit(active_indicator, ((x * 16) + (x * 2) + 1, (y * 16) + (y * 2) + 1))
                surface.blit(active_indicator_inner, ((x * 16) + (x * 2) + 2, (y * 16) + (y * 2) + 2))
            surface.blit(tiles[y * tiles_per_row + x], ((x * 16) + (x * 2) + 2, (y * 16) + (y * 2) + 2))
    
    for tile_pos in painted_tiles.keys():
        pos = tile_pos.split(";")
        canvas.blit(painted_tiles[tile_pos], ((int(pos[0]) * 16) + canvas_offset[0], (int(pos[1]) * 16) + canvas_offset[1]))

    canvas_origin.fill((255, 255, 255))

    origin_position = (
        ((((canvas.get_width() // 2) // 16) * 16) - 1) + canvas_offset[0] + (((canvas.get_width() // 2) // 16) * 16)
        ,
        ((((canvas.get_height() // 2) // 16) * 16) - 1) + canvas_offset[1] + (((canvas.get_height() // 2) // 16) * 16)
    )

    canvas.blit(canvas_origin, origin_position)

    surface.blit(canvas, ((tiles_per_row * 16) + 18, 0))


def update(dt: float):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        canvas_offset[1] += 1
    if keys[pygame.K_a]:
        canvas_offset[0] += 1
    if keys[pygame.K_s]:
        canvas_offset[1] -= 1
    if keys[pygame.K_d]:
        canvas_offset[0] -= 1


def event_handler(event: pygame.Event):
    global active_tile
    global fullscreen
    global running
    global window
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_PAGEDOWN:
            active_tile += 1 if active_tile + 1 != len(tiles) else 0
        if event.key == pygame.K_PAGEUP:
            active_tile -= 1 if active_tile > 0 else 0
        if event.key == pygame.K_F11:
            fullscreen = not fullscreen
            if fullscreen:
                window = pygame.display.set_mode((window_width, window_height), pygame.SCALED | pygame.FULLSCREEN, 0, 0, 0)
            else:
                window = pygame.display.set_mode((window_width, window_height), pygame.SCALED, 0, 0, 0)
        if event.key == pygame.K_ESCAPE:
            running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            relative_event_pos: tuple[int, int] = (event.pos[0] - sidenav.get_width() - canvas_offset[0], event.pos[1] - canvas_offset[1])
            tile_pos = [relative_event_pos[0] // 16, relative_event_pos[1] // 16]
            if f"{tile_pos[0]};{tile_pos[1]}" not in painted_tiles.keys():
                painted_tiles[f"{tile_pos[0]};{tile_pos[1]}"] = tiles[active_tile]
        if event.button == 3:
            relative_event_pos: tuple[int, int] = (event.pos[0] - sidenav.get_width() - canvas_offset[0], event.pos[1] - canvas_offset[1])
            tile_pos = [relative_event_pos[0] // 16, relative_event_pos[1] // 16]
            if f"{tile_pos[0]};{tile_pos[1]}" in painted_tiles.keys():
                painted_tiles.pop(f"{tile_pos[0]};{tile_pos[1]}")


def main():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            event_handler(event)

        dt = clock.tick(fps) / 1000

        screen.fill((0, 0, 0))

        render(screen)
        update(dt)
        
        pygame.display.update()


if __name__ == "__main__":
    main()
