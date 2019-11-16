"""
This file contains the methods and functions needed to visualize the results of
the fire spreading model.

@Authors: Max Dietrich
"""

import time
import pygame
import map


class View:
    """
    Contain all the methods needed to draw and update the screen showing the
    outcome of the model.
    """
    def __init__(self, width, height):
        """
        Initialize a screen
        """
        self.size = (width, height)
        self.screen = pygame.display.set_mode((width, height))

    def init_render(self, seed_map):
        """
        Render each tile as a green pixel prior to any burning
        """
        self.screen.fill((255, 255, 255))
        rect_dict = {}
        for coordinate in seed_map.tile_dict:
            rectangle = pygame.Rect((coordinate[0], coordinate[1]), (1, 1))
            rect_dict[coordinate] = rectangle
            pygame.draw.rect(self.screen, (34, 139, 34), rectangle)
        pygame.display.flip()
        time.sleep(0.01)

    def make_burning(self):
        """
        Update the color of each rectangle that is newly on fire
        """
        pass

    def make_extinguished(self):
        """
        Update the color of each rectangle that is newly extinguished
        """
        pass

    def update_render(self):
        """
        Cumulative updating method
        """
        pass

def draw_model():
    """
    Run the view functions.  Likely will be moved into calculate_fire.
    """
    sim_map = map.Map()
    sim_map.fromJSON('test_map')
    last_key = max(sim_map.tile_dict)
    view = View(last_key[0], last_key[1])
    view.init_render(sim_map)
    print('done')
    while True:
        view.update_render()





draw_model()
