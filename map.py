"""
Create a map class and its subclasses

@Authors: Max Dietrich
"""

class Map:
    """
    Store information for the entire map
    """
    def __init__(self, burning_dict=None, flammability_dict=None, fuel_dict=None, weather=None):
        """
        create a dictionary mapping each tile to a value representing if it is on fire and another dictionary mapping each tile to a flammability.  Also initializes global weather.
        """
        self.fire_dicts = burning_dict
        self.flammability_dict = flammability_dict
        self.fuel_dict = fuel_dict
        self.weather = Weather()

class Flammability:
    """
    create information about the flammability of an area
    """
    def __init__(self, flam_value=0, fuel_value=0):
        """
        Assigns a number between 0 and 100 to represent the flammability and fuel content of an area
        """
        self.flammability = flam_value
        self.fuel = fuel_value

class Weather:
    """
    Create information about the weather in this area
    """
    def __init__(self, wind_speed=0, wind_direction=0):
        self.wind = (wind_speed,wind_direction)
