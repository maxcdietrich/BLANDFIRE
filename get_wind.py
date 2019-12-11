"""
This file reads ESRI shapefiles containing wind data tagged to specific
locations on earth with UTM coordinates

    - In general, shapefiles have SHAPE and RECORD components
    - The RECORDS of the file passed into this function should organize data
        such that the 0th entry in each record is the magnitude of the wind
        speed, and the 3th entry is the direction

A Wind class is created to handle the parsing of these shapefiles with minimal
computational effort. Each method is documented individually.

To install necessary libraries:
pip install pyshp

link to pyshp documentation:
https://pypi.org/project/pyshp/

Link to resource about shapefiles:
https://en.wikipedia.org/wiki/Shapefile

@Authors: Shawn Albertson, Max Dietrich
"""
# Get shapefile from pyshp
import shapefile



class Wind:
    """
    Reads a ESRI shapefile containing wind data specified at a particular location
    Shapefiles are composed of a .shp and a .dbf file
    myshp: .shp file associated with shapefile
    mydbf: .dbf file associated with shapefile

    Requires input corresponding to latitude and longitude bounding coordinates
    """
    def __init__(self, myshp, mydbf, west_lon, east_lon, south_lat, north_lat):
        """
        Initializes Wind class using .Reader method from shapefile
        """
        self.reader = shapefile.Reader(shp = myshp, dbf = mydbf)

# The following four coordinate inputs must be obtained outside of the scope of the program. Go to
# https://www.engineeringtoolbox.com/utm-latitude-longitude-d_1370.html
# Then, call the method bounding_box to see the bounding UTM coordinates of the
# data collected. Enter the bounding coordinates into the calculator to find the
# corresponding latitude and longitude values. These will be used later to
# integrate with other parts of the code.

# This step is necessary because accurately location constrained data
# acquisition is not always possible.

        self.west_lon = west_lon
        self.east_lon = east_lon
        self.south_lat = south_lat
        self.north_lat = north_lat

# Get shapes objects which include information such as location and grid size
        self.shapes = self.reader.shapes()
# Get record objects containing wind data
        self.records = self.reader.records()
# Get number of datum
        self.length = len(self.shapes)


    def bounding_box(self):
        """
        Serves as a container for the bounding coordinates of the area of interest
        Returns 2 length list where each element is a four-tuple
        The first tuple defines longitudes, the second defines latitudes

        The first two elements in each tuple should be used when acquiring
        coordinates from
        https://www.engineeringtoolbox.com/utm-latitude-longitude-d_1370.html
        to be used when initializing a wind class
        """
# first_point and last_point contain UTM coordinates from self.shapes that
# correspond to top left and bottom right squares in the geographic grid
        first_point = self.shapes[0].points[0]
        last_point = self.shapes[len(self.shapes)-1].points[0]

# The 0th element in each coord pair describes longitude
        west_UTM = first_point[0]
        east_UTM = last_point[0]

# The 1th element in each coord pair describes latitude
        north_UTM = first_point[1]
        south_UTM = last_point[1]

        return [(west_UTM, east_UTM, self.west_lon, self.east_lon), (south_UTM, north_UTM, self.south_lat, self.north_lat)]

    def get_locations(self):
        """
        Returns list of (easting, northing) coordinate pairs
        """
# Define empty list for adding coordinate pairs
        locs = []

# Iterate over an index value defined by length of self.shapes
        for n in range(len(self.shapes)):

# Values returned as list contained in a list, index 0 to access the inner list
            loc = self.shapes[n].points[0]

# Add each element of list to locs, where each entry is a tuple
            locs.append((loc[0], loc[1]))

        return locs

    def convert_to_lon_lat(self):
        """
        Takes in desired bounding lat/lon coordinates and remaps UTM coordinates to these
        Returns two lists: latitudes, longitudes
        """
# Call get_locations to get unedited list of UTM coordinates
        raw = self.get_locations()

# Make the list of four-tuples to use as bounds in remap_interval
        bounds = self.bounding_box()

# Initialize lists to store lons and lats separately
        lons = []
        lats = []

# Iterate through list of tuples from raw
        for lon, lat in raw:

# At every entry, call remap_interval and add it to the lons and lats lists
            new_lon = remap_interval(lon, bounds[0][0], bounds[0][1], bounds[0][2], bounds[0][3])
            new_lat = remap_interval(lat, bounds[1][0], bounds[1][1], bounds[1][2], bounds[1][3])
            lons.append(new_lon)
            lats.append(new_lat)

        return lons, lats


    def get_wind_speeds(self):
        """
        Returns two lists: the wind speed in m/s, and their directions

        Direction is an angle equal to 0 at due north and increasing in the clockwise direction
        """
        recs = self.records

# Initialize lists for speed and direction
        speeds = []
        directions = []

# Iterate over index based on amount of data
        for n in range(len(recs)):

# For every record, add 0th element to speed and 3th element to direction
            speeds.append(self.records[n][0])
            directions.append(self.records[n][3])

        return speeds, directions

    def get_wind(self, input_lower_lon, input_upper_lon, input_lower_lat, input_upper_lat):
        """
        Only takes data that falls in target lat/lon range

        Crops the raw data to only include the specified locations

        input_lower_lon: desired west bounding longitude in decimal coordinates
        input_upper_lon: desired east bounding longitude in decimal coordinates
        input_lower_lat: desired south bounding longitude in decimal coordinates
        input_upper_lat: desired north bounding longitude in decimal coordinates
        """

# Call convert_to_lon_lat and get_wind_speeds methods to access geographic
# location and wind data
        lons, lats = self.convert_to_lon_lat()
        speeds, dirs = self.get_wind_speeds()

# Initialize wind data list
        wind_data = []

# Iterate over lists
        for n in range(len(lons)):

# Check to see if an element falls within the bounding box. If yes, add to list
            if lons[n] >= input_lower_lon and lons[n] <= input_upper_lon and lats[n] >= input_lower_lat and lats[n] <= input_upper_lat:
                wind_data.append((speeds[n], dirs[n]))

# Return list of speed, direction, where locations are now ignored
        return wind_data

    def find_base_size(self):
        """
        Looks at the size of the UTM scale used in the .shp file to find out how
        large each section is in meters. Also calculates the size of the rectangular
        grid bounding the area.

        Returns: grid size
        """

# Find longitudinal locations of first two points
        first_UTM = self.shapes[0].points[0][0]
        second_UTM = self.shapes[1].points[0][0]

# Find the difference. This difference in meters is the size of the grid
        grid_size = second_UTM - first_UTM

        return grid_size

    def regrid(self, new_size, input_lower_lon, input_upper_lon, input_lower_lat, input_upper_lat):
        """
        Takes an already calculated data set and projects it onto the desired
        size grid.

        For example, a data set represented in a 2x2 array could be scaled by a
        factor of 2 in each direction into a 4x4 array. Each value of a cell in
        the original 2x2 array would now occupy a 2x2 region of cells in the new
        array.

        New_size: int representing desired grid size in meters
        input_lower_lon: desired west bounding longitude in decimal coordinates
        input_upper_lon: desired east bounding longitude in decimal coordinates
        input_lower_lat: desired south bounding longitude in decimal coordinates
        input_upper_lat: desired north bounding longitude in decimal coordinates
        """
# Get grid size in meters
        old_size = self.find_base_size()

# Scaling factor is the ratio between the old size and the new size. If the
# ratio is 4, than 16 times as many squares will be added to the new grid
        scaling_factor = old_size / new_size

# Call wind_data to get 1D of data in a 2D space.
        wind_data = self.get_wind(input_lower_lon, input_upper_lon, input_lower_lat, input_upper_lat) #gather the wind data

# Split wind_data into a list of lists where each list represents data for one row
# The second input is hard coded based upon reasonable factor pairs of the total
# length of the data
        wind_data = list(split_list(wind_data, 359))
        new_grid = []
        for sub_list_id, sub_list in enumerate(wind_data): #work through the old data set one row at a time
            counter = 0
            while counter < scaling_factor: #repeate this operation for scaling factor number of columns
                for id, val in enumerate(sub_list):
                    if (id + 1) % 359 != 0: #i.e. not exceeded row length
                        new_grid.extend([sub_list[id]] * int(scaling_factor)) #add the old value scaling factor number of times in one the row
                    else:
                        counter = counter + 1
        return new_grid


def remap_interval(val,
        input_interval_start,
        input_interval_end,
        output_interval_start,
        output_interval_end):

    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
    val: the value to remap
    input_interval_start: the start of the interval that contains all
    possible values for val
    input_interval_end: the end of the interval that contains all possible
    values for val
    output_interval_start: the start of the interval that contains all
    possible output values
    output_interval_end: the end of the interval that contains all possible
    output values

    Returns:
    The value remapped from the input to the output interval

    Examples:
    >>> remap_interval(0.5, 0, 1, 0, 10)
    5.0
    >>> remap_interval(5, 4, 6, 0, 2)
    1.0
    >>> remap_interval(5, 4, 6, 1, 2)
    1.5
    >>> remap_interval(7, 3, 8, 0, 1)
    0.8
    """
    # Assumes that input_interval_end > input_interval_start
    # and output_interval_end > output_interval_start

    diff1 = input_interval_end-input_interval_start
    diff2 = output_interval_end-output_interval_start

    # Finds the variation in range size as a ratio
    ratio = diff2/diff1

    return output_interval_start + ratio*(val-input_interval_start)

def split_list(input_list, result_length):
    """
    Split a list into lists of result_length
    """
# Convert input to int type
    result_length = int(result_length)

# Use yield to hold the lists and compile them until the loop is done iterating
    for i in range(0, len(input_list), result_length):
        yield input_list[i:i+result_length]

def generate_wind():
    """
    This function serves as a wrapper to contain the values necessary for initializing
    a Wind class, and creates that class

    It then trims that class to desired coordinates and returns the list of
    wind data in the specified region
    """
# Taken by converting UTM Zone 11 coordinates on
# https://www.engineeringtoolbox.com/utm-latitude-longitude-d_1370.html
# These values specific to files called yosemite_landscape_12-03-2019_0900_120m
    west_lon = -120.006255
    east_lon = -119.4736
    south_lat = 37.464649
    north_lat = 37.822073

# Open .shp and .dbf files with rb
    myshp = open("SHAPEFILES/HOUR1/yosemite_landscape_12-03-2019_0900_120m.shp", "rb")
    mydbf = open("SHAPEFILES/HOUR1/yosemite_landscape_12-03-2019_0900_120m.dbf", "rb")
    wind = Wind(myshp, mydbf, west_lon, east_lon, south_lat, north_lat)

# Regrid the base data onto a 30mx30m grid and bounded at the coordinates described
# Our model focuses on the area between -120W to -119.5W, and 37.5N to 37.8N
    new_wind = wind.regrid(30, -120, -119.5, 37.5, 37.8)
    return new_wind

print(generate_wind())
