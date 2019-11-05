"""
This program should cacluate whether a tile adjacent to a tile on fire tile should also catch on fire.  It should also determine whether a tile on fire should remain on to be on fire.  This program must update the map information with the new result

@Author: Max Dietrich
"""
import Map
from random import randint

def catch_on_fire(center):
    """
    Generates a random chance for each cell adjacent to a cell on fire to catch on fire with a threshold given by a cell's flammability

    ISSUES:
    -Will break for edge cells
    Cannot distinguish cells that were on fire but are not anymore.  might reignite them
    """
    up_left = (center[0]-1, center[1]+1)
    up = (center[0], center[1]+1)
    up_right = (center[0]+1, center[1]+1)
    left = (center[0]-1, center[1])
    right = (center[0]+1, center[1])
    down_left = (center[0], center[1]-1)
    down = (center[0], center[1]-1)
    down_right = (center[0]+1, center[1]-1)
    cells_to_check = [up_left, up, up_right, left, right, down_left, down, down_right]
    for cell in cells_to_check:
        roll = randint(0,100)
        if roll < map.flammability_dict(cell):
            map.burning_dict(cell) = 1

def put_out(center):
    """
    Generates a fixed random chance for a cell on fire to stop being on fire
    """
    roll = randint(1,100)
    if roll > 80:
        map.burning_dict(center) = 0
