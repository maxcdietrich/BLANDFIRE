"""
pip install pyshp
"""

import shapefile

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



myshp = open("SHAPEFILES/HOUR1/yosemite_landscape_12-03-2019_0900_120m.shp", "rb")
mydbf = open("SHAPEFILES/HOUR1/yosemite_landscape_12-03-2019_0900_120m.dbf", "rb")


# Taken by converting UTM Zone 11 coordinates on https://www.ngs.noaa.gov/NCAT/
# These values specific to .shp files with preface "final_shape"
west_lon = -119.9940268086
east_lon = -119.4842024547

south_lat = 37.4548996589
north_lat = 37.8276271233


class Wind:
    """
    Reads a ESRI shapefile containing wind data specified at a particular location
    Shapefiles are composed of a .shp and a .dbf file
    myshp: .shp file associated with shapefile
    mydbf: .dbf file associated with shapefile

    Requires input corresponding to latitude and longitude bounding coordinates
    """
    def __init__(self, myshp, mydbf, west_lon, east_lon, south_lat, north_lat):
        self.reader = shapefile.Reader(shp = myshp, dbf = mydbf)
        self.west_lon = west_lon
        self.east_lon = east_lon
        self.south_lat = south_lat
        self.north_lat = north_lat

        self.shapes = self.reader.shapes()
        self.records = self.reader.records()

        self.length = len(self.shapes)


    def bounding_box(self):
        """
        Serves as a container for the bounding coordinates of the area of interest
        Returns 2 length list where each element is a four tuple
        The first tuple defines longitudes, the second defines latitudes
        """
        first_point = self.shapes[0].points[0]
        last_point = self.shapes[len(self.shapes)-1].points[0]

        west_UTM = first_point[0]
        east_UTM = last_point[0]

        # Read the file to get UTM latitude bounds
        north_UTM = first_point[1]
        south_UTM = last_point[1]

        return [(west_UTM, east_UTM, self.west_lon, self.east_lon), (south_UTM, north_UTM, self.south_lat, self.north_lat)]

    def get_locations(self):
        """
        Returns list of (easting, northing) coordinate pairs
        """

        locs = []
        for n in range(len(self.shapes)):
            loc = self.shapes[n].points[0]
            locs.append((loc[0], loc[1]))
        return locs

    def convert_to_lon_lat(self):
        """
        Takes in desired bounding lat/lon coordinates and remaps UTM coordinates to these
        Returns two lists: latitudes, longitudes
        """

        raw = self.get_locations()

# Make the list of four tuples to use as bounds in remap_interval
        bounds = self.bounding_box()
        lons = []
        lats = []
        for lon, lat in raw:
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
        speeds = []
        directions = []

        for n in range(len(recs)):
            speeds.append(self.records[n][0])
            directions.append(self.records[n][3])

        return speeds, directions

    def get_wind(self, input_lower_lon, input_upper_lon, input_lower_lat, input_upper_lat):
        """
        Only takes data that falls in target lat/lon range

        Crops the raw data to only include the specified locations
        """
        lons, lats = self.convert_to_lon_lat()
        speeds, dirs = self.get_wind_speeds()
        wind_data = []
        for n in range(len(lons)):
            if lons[n] >= input_lower_lon and lons[n] <= input_upper_lon and lats[n] >= input_lower_lat and lats[n] <= input_upper_lat:
                wind_data.append((speeds[n], dirs[n]))
        return wind_data

    def find_base_size(self):
        """
        Looks at the size of the UTM scale used in the .shp file to find out how
        large each section is in meters. Also calculates the size of the rectangular
        grid bounding the area.

        Returns: grid size
        """

        first_UTM = self.shapes[0].points[0][0]
        second_UTM = self.shapes[1].points[0][0]

        grid_size = second_UTM - first_UTM

        # Longitudinal grid dimension, latitudinal grid dimension:
        # Divide the first and last lon/lat values by the size of the grid, add
        # 1 to determine the total number of squares in each dimension
        lon_dim = (self.shapes[-1].points[0][0]-self.shapes[0].points[0][0]) / grid_size + 1
        lat_dim = (self.shapes[-1].points[0][1]-self.shapes[0].points[0][1]) / grid_size + 1

        return grid_size, lon_dim, lat_dim

    def regrid(self, new_size, input_lower_lon, input_upper_lon, input_lower_lat, input_upper_lat):
        """
        Takes an already calculated data set and projects it onto the desired size grid
        """

        old_size, lon_dim, lat_dim = self.find_base_size()

        scaling_factor = old_size / new_size

        wind_data = self.get_wind(input_lower_lon, input_upper_lon, input_lower_lat, input_upper_lat)


        new_grid = [0] * int(len(wind_data)) * int(scaling_factor)**2

        wind_data = list(split_list(wind_data, lon_dim))
        print(len(wind_data[1]), len(wind_data[0]), len(wind_data))
        new_list = []
        for ido, sub_list in enumerate(wind_data):
            counter = 0
            while counter < scaling_factor:
                for id, val in enumerate(sub_list):
                    if (id + 1) % lon_dim != 0:
                        new_list.extend([sub_list[id]] * int(scaling_factor))
                    else:
                        counter = counter + 1
            print('rolling over counter', ido)
        # for id, el in enumerate(new_grid):
        #     new_grid[id] = wind_data[int(id/(scaling_factor**2))]

        new_grid = new_list
        return new_grid

def split_list(input_list, result_length):
    """
    Split a list into a list of lists, each with length result_length
    """
    result_length = int(result_length)
    for i in range(0, len(input_list), result_length):
        yield input_list[i:i+result_length]

# Everything that has to do with shapes
def generate_wind():
    wind = Wind(myshp, mydbf, west_lon, east_lon, south_lat, north_lat)
    new_wind = wind.regrid(30, -120, -119.5, 37.5, 37.8)
    print(len(new_wind))
    return new_wind
    # print(new_wind[-30:-1])

generate_wind()
