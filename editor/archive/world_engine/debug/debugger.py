from world_engine.utils.imports import *
from world_engine.font.font import Font


class Debugger:
    def __init__(self, font_path, config) -> None:
        self.config = config

        self.screen = pygame.display.get_surface()
        self.surface = pygame.Surface(size=(pygame.display.get_surface().get_width() // (self.config.screen_multiplier // self.config.display_surface_multiplier), pygame.display.get_surface().get_height() // (self.config.screen_multiplier // self.config.display_surface_multiplier))).convert_alpha()
        self.rect = self.surface.get_rect(bottomright=self.screen.get_size())
        self.font = Font(path=font_path, size=self.config.font_size * 2, color=(255, 255, 255), config=self.config)
    

    def render(self) -> None:
        ...


    def draw(self) -> None:
        self.surface.fill(color=(100, 100, 100, 150))

        self.render(self)

        surface = pygame.transform.scale(self.surface, (self.screen.get_width() // 2, self.screen.get_height() // 2))
        rect = surface.get_rect(bottomright=self.screen.get_size())

        self.screen.blit(source=surface, dest=rect)
