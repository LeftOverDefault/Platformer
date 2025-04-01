from world_engine.utils.imports import *


class Font:
    def __init__(self, path, size, color, config) -> None:
        self.spacing = 1
        self.character_order = config.font_order
        font_img = pygame.image.load(path).convert_alpha()
        current_char_width = 0
        self.characters = {}
        character_count = 0

        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = self.clip(surface=font_img, x=x - current_char_width, y=0, x_size=current_char_width, y_size=font_img.get_height())
                char_img.fill(color=(0, 0, 0, 255), rect=None, special_flags=pygame.BLEND_RGBA_MULT)
                char_img.fill(color=color[0:3] + (0,), rect=None, special_flags=pygame.BLEND_RGBA_ADD)
                char_img = pygame.transform.scale_by(surface=char_img, factor=size)
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_width()
        self.line_height = self.characters["A"].get_height() + 4


    def clip(self, surface: pygame.Surface, x, y, x_size, y_size):
        handle_surface = surface.copy()
        clip_rect = pygame.Rect(x, y, x_size, y_size)
        handle_surface.set_clip(clip_rect)
        image = surface.subsurface(handle_surface.get_clip())
        return image.copy()


    def render(self, surface: pygame.Surface, text, location):
        x_offset = 0
        for char in text:
            if char != " ":
                surface.blit(source=self.characters[char], dest=(location[0] + x_offset, location[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
    

    def return_image(self, text):
        x_offset = 0
        text_images = []
        for char in text:
            if char != " ":
                text_images.append([self.characters[char], x_offset])
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
        return text_images
