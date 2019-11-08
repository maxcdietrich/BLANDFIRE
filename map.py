"""
Create a map class and its subclasses

@Authors: Max Dietrich
"""

class Map:
    """
    Store information for the entire map
    """
    def __init__(self, tile_dict={}):
        """
        create a dictionary mapping each tile to an x,y tuple
        """
        self.tile_dict = tile_dict

class Tile:
    def __init__(self, is_burning=False, flammability=0, fuel=0, weather=None, rain=None, elevation=0):
        """
        Initiate the information for a tile
        """
        self.is_burning = is_burning
        self.flammability = flammability #0-100
        self.fuel = fuel #0-100
        self.wind = wind #should be a vector quantity
        self.rain = rain #IMPLEMENT
        self.elevation = elevation #IMPLEMENT (Scalar? Gradient?)
