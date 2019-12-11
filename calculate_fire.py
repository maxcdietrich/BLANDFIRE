"""
This program cacluates whether a tile adjacent to a tile on fire tile
should also catch on fire.  It also determines whether a tile on fire
should remain on fire.  This program also updates the map information
with the new results and calls the functions needed to update the visuals

@Authors: Max Dietrich
"""
import math
from random import randint
import map
import render


def catch_on_fire(center, data_map):
    """
    Given the input cell "center", and the rest of the map "data_map", calculate whether each tile adjacent to center should catch on fire
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
        for id, cell in enumerate(cells_to_check):
            if data_map.tile_dict[cell].is_burning == False: #Only try to ignite cell if it is not on fire
                const_factor = 0.04

                wind_factor = math.exp(0.045 * data_map.tile_dict[center].wind[0]) * math.exp(data_map.tile_dict[center].wind[0] * 0.131 * (math.cos(data_map.tile_dict[center].wind_components[id] * math.pi/180) -1))

                flam_factor =  1 + data_map.tile_dict[cell].flammability / 100

                fuel_factor = 1 + data_map.tile_dict[cell].flammability / 100

                elevation_factor = math.exp(0.078 * math.atan(data_map.tile_dict[center].slope[id]))

                ignition_probability = const_factor * (1+flam_factor) * (1+fuel_factor) * wind_factor * elevation_factor #create the probability of the adjacent cell catching on fire

                roll = randint(0, 100) #create a random roll to check for fire spread
                if roll < ignition_probability*100: #compare the roll to the ignition_probability
                    data_map.tile_dict[cell].is_burning = True #the adjacent cell catches on fire
                    new_burning_cells.append(cell)
    except KeyError: #I.E. the target cell is not in the map
        pass
    return new_burning_cells

def put_out(center, real_map):
    """
    Generates a random roll and extinguishes the fire if it is higher than the
    tile fuel value.  If not, decrease the fuel value to make it more likely to
    be extinguished
    """
    roll = randint(-40, 40)
    if roll > real_map.tile_dict[center].fuel:
        real_map.tile_dict[center].is_burning = False
        real_map.tile_dict[center].flammability = 0
        return True
    else:
        real_map.tile_dict[center].fuel = real_map.tile_dict[center].fuel - 1
        return False

def calculate_fire(current_burning_cells, current_extinguished_cells, real_map, view_object):
    """
    Acts as the controller for the program

    Iterate through a list containing the coordinates for burning cells and run
    the calculations on whether fire should spread or be put out.
    """
    burning_cell_update = [] #Initialize a list of newly_burning cells
    extinguished_cell_update = [] #Initialize a list of newly extinguished cells
    for cell in current_burning_cells:
        burning_cell_update.extend(catch_on_fire(cell, real_map)) #add the cells that catch on fire
        if put_out(cell,real_map):
            extinguished_cell_update.append(cell) #add the cells that are extinguished
    if len(current_burning_cells) == 0:
        print("The fire is out!")
        return
    current_burning_cells.extend(burning_cell_update)
    current_burning_cells = list(set(current_burning_cells) - set(extinguished_cell_update)) #remove any duplicates
    current_extinguished_cells.extend(extinguished_cell_update)
    view_object.update_render(burning_cell_update, extinguished_cell_update, real_map)
    return (current_burning_cells, current_extinguished_cells)


def run_model(iteration_limit):
    """
    Initialize the controller
    could add kwargs for user to specify many cells to initially be on fire
    """
    #need to add view functions here
    real_map = map.Map()
    real_map.fromJSON('real_map')
    last_key = max(real_map.tile_dict) #find the maximum x,y pair for sizing the display
    view = render.View(last_key[0], last_key[1])
    view.init_render(real_map)

    burning_cells = [(1000,800)] #initial burning cells
    extinguished_cells = [] #initial extinguished cells
    iteration = 0
    while iteration <= iteration_limit:
        try:
            burning_cells, extinguished_cells = calculate_fire(burning_cells, extinguished_cells, real_map, view) #DO NOT PASS IN map AS A PARAMETER
            iteration += 1
        except TypeError: #crash pygame gracefully
            return

run_model(5000)
