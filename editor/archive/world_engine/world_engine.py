from world_engine.classes.camera import Camera
from world_engine.classes.configure import Configure
from world_engine.debug.debugger import Debugger
from world_engine.func.json_export import json_export
from world_engine.func.json_import import json_import
from world_engine.interface.canvas import Canvas
from world_engine.interface.sidenav import Sidenav
from world_engine.utils.config import *
from world_engine.utils.imports import *


class WorldEngine:
    def __init__(self, config) -> None:
        pygame.init()
        pygame.display.set_caption(f"World Engine v{VERSION}")

        self.config = Configure(config)

        self.on_init()
        self.set_cursor()


    def on_init(self) -> None:
        self.screen = pygame.display.set_mode((198 * self.config.screen_multiplier, 108 * self.config.screen_multiplier))
        self.display_surface = pygame.Surface((198 * self.config.display_surface_multiplier, 108 * self.config.display_surface_multiplier))

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.running = True
        self.fullscreen = False

        self.camera = Camera(self.display_surface, self.config)
        self.canvas = Canvas(self.display_surface, self.camera, self.config)
        self.debugger = Debugger(self.config.font, self.config)
        self.sidenav = Sidenav(self.display_surface, self.config)

    
    def set_cursor(self):
        cursor_image = pygame.image.load("./world_engine/mouse.png").convert_alpha()
        cursor = pygame.Cursor((0, 0), cursor_image)
        pygame.mouse.set_cursor(cursor)

    
    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen == True:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((198 * self.config.screen_multiplier, 108 * self.config.screen_multiplier))
                    
                    elif event.key == pygame.K_e:
                        json_export(self.canvas.layers, self.config)
                    elif event.key == pygame.K_i:
                        json_import(self.camera, self.canvas, self.config)
                    elif event.key == pygame.K_c:
                        self.camera.empty()
                        for layer in self.canvas.layers:
                            layer.empty()
                            layer.tile_positions.clear()

                self.sidenav.get_current_tile()
                self.sidenav.get_current_layer()
                self.sidenav.scroll(event)

                self.canvas.create_tile(self.sidenav.current_tile, self.sidenav.current_layer)
                self.canvas.draw_tiles()

            self.delta_time = self.clock.tick(self.fps) / 1000

            self.display_surface.fill("#292d3e")

            self.camera.draw()
            self.camera.update(self.delta_time)

            pygame.draw.line(self.display_surface, "#52576c", (-self.camera.offset.x, (-self.camera.offset.y) - 5), (-self.camera.offset.x, (-self.camera.offset.y) + 5))
            pygame.draw.line(self.display_surface, "#52576c", ((-self.camera.offset.x) - 5, -self.camera.offset.y), ((-self.camera.offset.x) + 5, -self.camera.offset.y))

            self.sidenav.draw()

            self.screen.blit(pygame.transform.scale(self.display_surface, self.screen.get_size()), (0, 0))
            if self.config.debug == True:
                self.debugger.draw()

            pygame.display.update()
