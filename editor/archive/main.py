from world_engine import world_engine


config = {
    "screen_multiplier": 6,
    "display_surface_multiplier": 2,
    "tile_size": 16,
    "chunk_size": 8,
    "debug": False,
    "tilesets": {
        "tilesheet": "../src/assets/textures/tilesets/sunny_land.png"
    },
    "current_tileset": "tilesheet",
    "font": "./font.png",
    "font_colour": (255, 236, 250),
    "font_order": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ".", "-", ",", ":", "+", "'", "!", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", "/", "_", "=", "\\", "[", "]", "*", "\"", "<", ">", ";", "|", "~", "£", "ƒ", "{", "}", "@", "#", "$", "%", "&", "^", "`"],
    "font_size": 1,
    "world_name": "overworld",
    "layers": [
        "Layer_1",
        "Layer_2",
    ],
    "build_directory": "./worlds/"
}


def debug_render(self):
    self.font.render(surface=self.surface, text=f"Debug Menu:", location=(10, 10 + (0 * self.font.line_height)))
    self.font.render(surface=self.surface, text=f"FPS: {round(number=engine.clock.get_fps())}", location=(10, 10 + (1 * self.font.line_height)))
    self.font.render(surface=self.surface, text=f"Delta Time: {round(number=engine.delta_time, ndigits=4)}", location=(10, 10 + (2 * self.font.line_height)))


if __name__ == "__main__":
    engine = world_engine.WorldEngine(config=config)
    engine.debugger.render = debug_render
    engine.run()
