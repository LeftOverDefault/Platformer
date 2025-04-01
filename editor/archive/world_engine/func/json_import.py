from world_engine.classes.tile.canvas_tile import CanvasTile
from world_engine.classes.camera import Camera
from world_engine.classes.configure import Configure
from world_engine.classes.layer import Layer
from world_engine.func.import_cut_graphics import import_cut_graphics
from world_engine.interface.canvas import Canvas
from world_engine.utils.imports import *


def json_import(camera: Camera, canvas: Canvas, config: Configure):
    canvas.layers.clear()
    for _, __, layers in os.walk(f"{config.build_directory}"):
        for layer in layers:
            with open(f"{config.build_directory}{layer}", "r") as layer_file:
                layer_dict = json.load(layer_file)
                tileset = import_cut_graphics(config.tilesets[layer_dict["layer_tileset"]], config)
                current_layer = Layer()

                for chunk, chunk_data in layer_dict["layer_chunks"].items():
                    chunk_x = int(chunk.split(";")[0])
                    chunk_y = int(chunk.split(";")[1])

                    for tile, tile_value in chunk_data.items():
                        tile_x = (int(tile.split(";")[0]) + (chunk_x * config.chunk_size)) * config.tile_size
                        tile_y = (int(tile.split(";")[1]) + (chunk_y * config.chunk_size)) * config.tile_size

                        current_layer.tile_positions.append([tile_x // config.tile_size, tile_y // config.tile_size])

                        CanvasTile(tileset[tile_value], tile_value, (tile_x, tile_y), current_layer)

                canvas.layers.append(current_layer)
