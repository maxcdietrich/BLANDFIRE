"""
This program should cacluate whether a tile adjacent to a tile on fire tile
should also catch on fire.  It should also determine whether a tile on fire
should remain on to be on fire.  This program must update the map information
with the new result

@Authors: Max Dietrich
"""
from random import randint
import timeit
import matplotlib.pyplot as plt
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
            if test_map.tile_dict[cell].is_burning == False: #Only try to ignite cell if it is not on fire
                roll = randint(0, 100) #create a random roll to check for fire spread
                const_factor = 0.4
                wind_factor = 1
                flam_factor = test_map.tile_dict[cell].flammability / 100
                fuel_factor = 1
                elevation_factor = 1
                ignition_probability = const_factor*wind_factor*flam_factor*fuel_factor*elevation_factor #create the probability of the adjacent cell catching on fire
                if roll < ignition_probability*100: #compare the roll to the ignition_probability
                    test_map.tile_dict[cell].is_burning = True #the adjacent cell catches on fire
                    new_burning_cells.append(cell)
            else:
                pass
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
        test_map.tile_dict[center].fuel = test_map.tile_dict[center].fuel - 0.1
        return False

def calculate_fire(current_burning_cells, current_extinguished_cells, test_map, view_object):
    """
    Acts as the controller for the program

    Iterate through a list containing the coordinates for burning cells and run
    the calculations on whether fire should spread or be put out.  contains
    information on the current and previous states of burning and extinguished
    cells.  Runs for a number of steps specified by tick_limit
    """
    burning_cell_update = []
    extinguished_cell_update = []
    for cell in current_burning_cells:
        burning_cell_update.extend(catch_on_fire(cell, test_map))
        if put_out(cell, test_map):
            extinguished_cell_update.append(cell)
    if len(current_burning_cells) == 0:
        print("The fire is out!")
        return
    current_burning_cells.extend(burning_cell_update)
    current_burning_cells = list(set(current_burning_cells) - set(extinguished_cell_update))
    current_extinguished_cells.extend(extinguished_cell_update)
    view_object.update_render(burning_cell_update, extinguished_cell_update)
    return (current_burning_cells, current_extinguished_cells)







def run_model(iteration_limit):
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
    iteration = 0
    dataset_size = []
    runtime = []
    while iteration <= iteration_limit:
        start = timeit.default_timer()
        burning_cells, extinguished_cells = calculate_fire(burning_cells, extinguished_cells, test_map, view) #DO NOT PASS IN map AS A PARAMETER
        stop = timeit.default_timer()
        dataset_size.append(len(burning_cells))
        runtime.append(stop-start)
        iteration += 1

    plt.scatter(dataset_size, runtime)
    plt.xlabel('# of burning cells')
    plt.ylabel('calculate_fire runtime')
    plt.show()

run_model(500)
