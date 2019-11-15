"""
Create a map class and its subclasses

@Authors: Max Dietrich
"""

import json

class Map:
    """
    A low level object containing a dictionary.  Intended to map tuples with x,y data to Tile objects
    """
    def __init__(self, tile_dict={}):
        """
        Create a dictionary mapping each tile to an x,y tuple
        """
        self.tile_dict = tile_dict

    def __str__(self):
        """
        Will print map properly but then throw error.  could catch with exception if it becomes a problem
        """
        for key in self.tile_dict:
            print(key,'\n',self.tile_dict[key],'\n')

    def toJSONs(self):
        """
        Returns a json formatted string of self
        """
        return json.dumps(self,default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toJSON(self, filename):
        """
        Returns a json formatted .txt file of self
        """
        with open('{}.txt'.format(filename), 'w') as outfile:
            json.dump(self, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fromJSON(self, filename):
        """
        Returns a Map object from a properly formatted json .txt file.  The target file must be encoded in the same format as a map object.

        Inverse of toJSON
        """
        self.tile_dict={}
        with open('{}.txt'.format(filename), 'r') as infile:
            top_layer = json.load(infile)['tile_dict']
            for key in top_layer:
                tile_data = top_layer[key]
                tile = Tile(**tile_data)
                self.tile_dict[key] = tile
        return self.tile_dict


class Tile:
    def __init__(self, is_burning=False, flammability=0, fuel=0, wind=None, elevation=0):
        """
        Initiate the information for a tile
        """
        self.is_burning = is_burning
        self.flammability = flammability #0-100
        self.fuel = fuel #0-100
        self.wind = wind #should be a vector quantity
        self.elevation = elevation

    def __str__(self):
        burning = 'is_burning ='+str(self.is_burning)+'\n'
        flammability = 'flammability ='+str(self.flammability,)+'\n'
        fuel = "fuel ="+str(self.fuel)+'\n'
        elevation = "elevation ="+str(self.elevation)
        return burning+flammability+fuel+elevation
