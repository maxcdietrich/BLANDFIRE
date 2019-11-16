"""
This program should cacluate whether a tile adjacent to a tile on fire tile should also catch on fire.  It should also determine whether a tile on fire should remain on to be on fire.  This program must update the map information with the new result

@Authors: Max Dietrich
"""
import map
from random import randint

def catch_on_fire(center):
    """
    Calculate the probabilty for a cell on fire to light its adjacent cells on fire
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
    new_burning_cells = []
    for cell in cells_to_check:
        roll = randint(0,100) #create a random roll to check for fire spread
        const_factor = 0.58
        wind_factor = 1
        flam_factor = 1
        fuel_factor = 1
        elevation_factor = 1
        ignition_probability = const_factor*wind_factor*flam_factor*fuel_factor*elevation_factor #create the probability of the adjacent cell catching on fire
        if roll < ignition_probability*100: #compare the roll to the ignition_probability
            map.tile_dict(cell).is_burning = True #the adjacent cell catches on fire
            new_burning_cells.append(cell)
    return new_burning_cells

def put_out(center):
    """
    Generates a random roll and extinguishes the fire if it is higher than the tile fuel value
    """
    roll = randint(1,100)
    if roll > map.tile_dict(center).fuel:
        map.tile_dict(ceter).is_burning = False
        map.tile_dict(center).flammability = 0
        return True
    else:
        map.tile_dict(center).fuel = map.tile_dict(center).fuel - 1
        return False



def calculate_fire(start_tick, tick_limit, previous_burning_cells, previous_extinguished_cells):
    """
    Iterate through a list containing the coordinates for burning cells and run the calculations on whether fire should spread
    """
    #need to add view functions here
    if start_tick >= tick_limit:
        return previous_burning_cells
    else:
        current_burning_cells = set(previous_burning_cells)
        current_extinguished_cells = set(previous_extinguished_cells)
        for cell in previous_burning_cells:
            assert type(cell) == tuple
            new_burning_cells = catch_on_fire(cell)
            current_burning_cells = set(current_burning_cells.extend(new_burning_cells))
            if put_out(cell):
                current_burning_cells.remove(cell)
                current_extinguished_cells.append(cell)
        current_burning_cells.sort()
        current_extinguished_cells.sort()
        start_tick = start_tick + 1
        calculate_fire(start_tick, tick_limit, current_burning_cells, current_extinguished_cells)


def run_model(tick_limit):
    """
    Can add kwargs for user to specify many cells to initially be on fire
    """
    #need to add view functions here
    burning_cells = []
    extinguished_cells = []
    calculate_fire(0, tick_limit, burning_cells, extinguished_cells)
