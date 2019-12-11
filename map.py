"""
Create a map class and its subclasses to store all necessary data about the region of interest.

@Authors: Max Dietrich
"""

import json

class Map:
    """
    A top level object containing a dictionary.
    Intended to map tuples with x,y position to Tile objects
    """
    def __init__(self, tile_dict={}):
        """
        Create a dictionary mapping each tile to an x,y tuple
        """
        self.tile_dict = tile_dict

    def __str__(self):
        string = ""
        for key in self.tile_dict:
            string += str(key) + '\n' + self.tile_dict[key].__str__() + '\n\n'
        return string

    def toJSONs(self):
        """
        Returns a json formatted string of self
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toJSON(self, filename):
        """
        Returns a json formatted .txt file of self
        """
        with open('{}.txt'.format(filename), 'w') as outfile:
            json.dump(self, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self, filename):
        """
        Returns a Map object from a properly formatted json .txt file.
        The target file must be encoded in the same format as a map object.

        Inverse of toJSON
        """
        self.tile_dict = {}
        with open('{}.txt'.format(filename), 'r') as infile:
            top_layer = json.load(infile)['tile_dict']
            for key in top_layer:
                tile_data = top_layer[key]
                tile = Tile(**tile_data)
                self.tile_dict[eval(key)] = tile
        return self.tile_dict


class Tile:
    """
    The base unit of the map and our model is the tile.
    This contains information for a small geographic area
    """
    def __init__(self, is_burning=False, flammability=0, fuel=0, wind=None, wind_components=None, elevation=0, slope=None):
        """
        Initiate the information for a tile
        """
        self.is_burning = is_burning
        self.flammability = flammability #0-100
        self.fuel = fuel #0-100
        self.wind = wind #should be a vector quantity
        self.wind_components = wind_components #Should be a list of wind angle to the direction of each adjacent cell
        self.elevation = elevation
        self.slope = slope #should be a list of slope to each adjacent tile from the perspective of this tile

    def __str__(self):
        burning = 'is_burning ='+str(self.is_burning)+'\n'
        flammability = 'flammability ='+str(self.flammability,)+'\n'
        fuel = "fuel ="+str(self.fuel)+'\n'
        elevation = "elevation ="+str(self.elevation)
        return burning+flammability+fuel+elevation
