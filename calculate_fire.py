"""
This program should cacluate whether a tile adjacent to a tile on fire tile
should also catch on fire.  It should also determine whether a tile on fire
should remain on to be on fire.  This program must update the map information
with the new result

@Authors: Max Dietrich
"""
from random import randint
import map
import render


def catch_on_fire(center, test_map):
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
    try: #Will try to check fire spread unless the target cell is not in the map
        for cell in cells_to_check:
            roll = randint(0, 100) #create a random roll to check for fire spread
            const_factor = 0.35
            wind_factor = 1
            flam_factor = test_map.tile_dict[cell].flammability / 100
            fuel_factor = 1
            elevation_factor = 1
            ignition_probability = const_factor*wind_factor*flam_factor*fuel_factor*elevation_factor #create the probability of the adjacent cell catching on fire
            if roll < ignition_probability*100: #compare the roll to the ignition_probability
                test_map.tile_dict[cell].is_burning = True #the adjacent cell catches on fire
                new_burning_cells.append(cell)
    except KeyError:
        pass
    return new_burning_cells

def put_out(center, test_map):
    """
    Generates a random roll and extinguishes the fire if it is higher than the
    tile fuel value.  If not, decrease the fuel value to make it more likely to
    be extinguished
    """
    roll = randint(1, 100)
    if roll > test_map.tile_dict[center].fuel:
        test_map.tile_dict[center].is_burning = False
        test_map.tile_dict[center].flammability = 0
        return True
    else:
        test_map.tile_dict[center].fuel = test_map.tile_dict[center].fuel - 1
        return False



def calculate_fire(start_tick, tick_limit, previous_burning_cells, previous_extinguished_cells, test_map, view_object):
    """
    Acts as the controller for the program

    Iterate through a list containing the coordinates for burning cells and run
    the calculations on whether fire should spread or be put out.  contains
    information on the current and previous states of burning and extinguished
    cells.  Runs for a number of steps specified by tick_limit
    """
    #need to add view functions here
    if start_tick >= tick_limit:
        return
    else:
        current_burning_cells = set(previous_burning_cells) #use sets to eliminate duplicate values.
        current_extinguished_cells = set(previous_extinguished_cells) #set the previous state to be the current state
        for cell in previous_burning_cells:
            assert type(cell) == tuple
            additional_burning_cells = set(catch_on_fire(cell, test_map))
            current_burning_cells |= additional_burning_cells #Union
            if put_out(cell, test_map): #improper use of methods with sets
                current_burning_cells.remove(cell) #remove cells that are extinguished
                current_extinguished_cells.add(cell) #add extinguised cells to this set
        current_burning_cells = sorted(current_burning_cells) #sort the lists so they are in a known order
        if len(current_burning_cells) == 0:
            print("The fire is out!")
            return
        current_extinguished_cells = sorted(current_extinguished_cells)
        new_burning_cells = list(set(current_burning_cells) - set(previous_burning_cells))
        new_extinguished_cells = list(set(current_extinguished_cells) - set(previous_extinguished_cells))
        start_tick = start_tick + 1
        view_object.update_render(new_burning_cells, new_extinguished_cells)
        calculate_fire(start_tick, tick_limit, current_burning_cells, current_extinguished_cells, test_map, view_object) #run with the current state as the previous state next iteration


def run_model(tick_limit):
    """
    Initialize the controller
    could add kwargs for user to specify many cells to initially be on fire
    """
    #need to add view functions here
    test_map = map.Map()
    test_map.fromJSON('test_map')

    last_key = max(test_map.tile_dict)
    view = render.View(last_key[0], last_key[1])
    view.init_render(test_map)

    burning_cells = [(300,300)]
    extinguished_cells = []
    calculate_fire(0, tick_limit, burning_cells, extinguished_cells, test_map, view) #DO NOT PASS IN map AS A PARAMETER

run_model(1000)
