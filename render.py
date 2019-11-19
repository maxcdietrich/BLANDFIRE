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
        self.rect_dict = {}

    def init_render(self, seed_map):
        """
        Render each tile as a green pixel prior to any burning
        """
        self.screen.fill((255, 255, 255))
        for coordinate in seed_map.tile_dict:
            rectangle = pygame.Rect((coordinate[0], coordinate[1]), (1, 1))
            self.rect_dict[coordinate] = rectangle
            pygame.draw.rect(self.screen, (34, 139, 34), rectangle)
        pygame.display.flip()
        time.sleep(0.01)

    def make_burning(self, burn_update):
        """
        Update the color of each rectangle that is newly on fire
        """
        for cell in burn_update:
            rectangle = self.rect_dict[cell]
            pygame.draw.rect(self.screen, (255, 0, 0), rectangle)
        pygame.display.flip()

    def make_extinguished(self, extinguish_update):
        """
        Update the color of each rectangle that is newly extinguished
        """
        for cell in extinguish_update:
            rectangle = self.rect_dict[cell]
            pygame.draw.rect(self.screen, (0, 0, 0), rectangle)
        pygame.display.flip()

    def update_render(self, burn_update, extinguish_update):
        """
        Cumulative updating method
        """
        self.make_burning(burn_update)
        self.make_extinguished(extinguish_update)
