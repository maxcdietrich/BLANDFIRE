"""
This file should create a Map object from the compiled data and then cache that map to a JSON formatted txt file

@Authors: Max Dietrich
"""
from random import randint
import math
import json
import map
import get_wind

south_west_corner = (37.5, -120) #coordinate pair
north_east_corner = (37.8, -119.5) #coordinate pair
x_length = 44190 #east-west length [m] ignore earth curvature
y_length = 33300 #north-south length [m]
# x_length = 15000 #Test values to make small map
# y_length = 15000 #Test values to make small map
tile_size = 30 #GIS tile 30m x 30m

#
# def make_random_map():
#     """
#     Define a random data set for testing the model
#     """
#     random_map = map.Map()
#     for x in range(x_length//tile_size):
#         for y in range(y_length//tile_size):
#             tile = map.Tile()
#             tile.is_burning = False
#             tile.flammability = randint(-40, 40) * math.cos(x /(300*math.pi))
#             tile.fuel = randint(-40, 40)
#             tile.wind = (1, 1) #speed, direction
#             tile.elevation = math.sin(x/(100*math.pi)) * 50 * math.sin(y/(100*math.pi)) #1D sine wave
#             random_map.tile_dict[str((x, y))] = tile #key is a str because json does not take tuples as keys
#     return random_map
#
# def write_random_map(filename):
#     """
#     Create a random map and write it to a text file in a JSON format
#     """
#     random_map = make_random_map()
#     random_map.toJSON(filename)


def load_elevation_data():
    elevation = json.loads(open('norm_elevation.json', 'r').read())
    slope = json.loads(open('slope.json', 'r').read())
    return elevation, slope


def make_real_map():
    real_map = map.Map()
    simulation_wind = get_wind.generate_wind() #get wind data
    elevation_data, slope_data = load_elevation_data()
    for y in range(y_length//tile_size):
        for x in range(x_length//tile_size):
            tile = map.Tile()
            tile.is_burning = False
            tile.flammability = randint(-40, 40) * math.cos(x /(300*math.pi))
            tile.fuel = randint(-40, 40)
            tile.wind = simulation_wind[(y * (y_length // tile_size) + x)] #convert 2d index to 1d index of wind_data
            tile.wind_components = [tile.wind[1]-45, tile.wind[1], tile.wind[1]+45, tile.wind[1]-90, tile.wind[1]+90, tile.wind[1]-135, tile.wind[1]-180, tile.wind[1]+135] #angle difference between wind direction and adjacent cell direction
            tile.elevation = elevation_data[str((y, x))]
            tile.slope = slope_data[str((y, x))]
            real_map.tile_dict[str((x, y))] = tile #key is a str because json does not take tuples as keys
    return real_map

def write_real_map(filename):
    """
    Create a random map and write it to a text file in a JSON format
    """
    real_map = make_real_map()
    real_map.toJSON(filename)


# write_random_map('test_map')
# load_elevation_data()
write_real_map('real_map')
