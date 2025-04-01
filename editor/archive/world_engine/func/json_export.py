from world_engine.utils.imports import *


def json_export(layers, config):
    for layer_index, layer in enumerate(layers):
        layer_name = config.layers[layer_index].lower()
        tile_positions = layer.tile_positions
        layer_dict = {
            "layer_name": layer_name,
            "layer_index": layer_index,
            "layer_tileset": config.current_tileset,
            "y-sorted": False,
            "collidable": False,
            "layer_chunks": {}
        }

        for sprite in layer:
            sprite_position = (sprite.rect.topleft[0] // config.tile_size, sprite.rect.topleft[1] // config.tile_size)
            sprite_index = sprite.tile_index

            sprite_chunk = f"{sprite_position[0] // config.chunk_size};{sprite_position[1] // config.chunk_size}"
            sprite_coordinate = f"{sprite.rect.topleft[0] // config.tile_size};{sprite.rect.topleft[1] // config.tile_size}"

            if sprite_chunk not in layer_dict["layer_chunks"].keys():
                layer_dict["layer_chunks"][sprite_chunk] = {}

                sprite_coordinate = f"{sprite_position[0] % 8};{sprite_position[1] % 8}"
                layer_dict["layer_chunks"][sprite_chunk][sprite_coordinate] = sprite_index

            else:
                sprite_coordinate = f"{sprite_position[0] % 8};{sprite_position[1] % 8}"
                layer_dict["layer_chunks"][sprite_chunk][sprite_coordinate] = sprite_index

        try:
            with open(f"{config.build_directory}{config.world_name}_{layer_name}.json", "x") as layer_file:
                json.dump(layer_dict, layer_file)
        except FileExistsError or FileNotFoundError:
            with open(f"{config.build_directory}{config.world_name}_{layer_name}.json", "w") as layer_file:
                json.dump(layer_dict, layer_file)
