from world_engine.utils.imports import *


def array_split(array, indicies):
    final_array = []
    array_length = len(array)

    if array_length == 0:
        return []
    
    for i in range(0, array_length, indicies):
        final_array.append(array[i:i + indicies])

    return final_array
