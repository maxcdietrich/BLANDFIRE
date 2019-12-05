"""
This file should create a Map object from the compiled data and then cache that map to a JSON formatted txt file

@Authors: Max Dietrich
"""
from random import randint
import math
import map

south_west_corner = (37.5, -120) #coordinate pair
north_east_corner = (37.8, -119.5) #coordinate pair
# x_length = 44190 #east-west length [m] ignore earth curvature
# y_length = 33300 #north-south length [m]
x_length = 15000 #Test values to make small map
y_length = 15000 #Test values to make small map
tile_size = 30 #GIS tile 30m x 30m


def make_random_map():
    """
    Define a random data set for testing the model
    """
    random_map = map.Map()
    for x in range(x_length//tile_size):
        for y in range(y_length//tile_size):
            tile = map.Tile()
            tile.is_burning = False
            tile.flammability = randint(-40, 40) * math.cos(x /(300*math.pi))
            tile.fuel = randint(-40, 40)
            tile.wind = (1, 1) #speed, direction
            tile.elevation = math.sin(x/(100*math.pi)) * 50 * math.sin(y/(100*math.pi)) #1D sine wave
            random_map.tile_dict[str((x, y))] = tile #key is a str because json does not take tuples as keys
    return random_map

def write_random_map(filename):
    """
    Create a random map and write it to a text file in a JSON format
    """
    random_map = make_random_map()
    random_map.toJSON(filename)

write_random_map('test_map')
