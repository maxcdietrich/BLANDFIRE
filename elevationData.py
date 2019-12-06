import gdal
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class elevation:

    def __init__(self,filename):
        """
        initialized an elevation class
        self.elevation_array = array of elevation data extracted from a .tif file
        self.norm_data_array = elevation data normalized between 0 and 255 for color visualization
        """
        data = gdal.Open(filename)
        band = data.GetRasterBand(1)
        no_data_val = band.GetNoDataValue()

        self.elevation_array = data.ReadAsArray().astype(np.float)
        if np.any(data == no_data_val):
            self.elevation_array[data == no_data_val] = np.nan

        self.norm_data_array = self.normalize()

    def display(self,resolution = 50):
        """
        Displays original data
        """
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        plt.contourf(self.elevation_array, cmap = "viridis",
                    levels = list(range(0, int(np.amax(self.elevation_array))+resolution, resolution)))
        plt.title("Yosemite")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def display_norm(self,resolution = 50):
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        plt.contourf(self.norm_data_array, cmap = "viridis",
                    levels = list(range(0, int(np.amax(self.norm_data_array))+resolution, resolution)))
        plt.title("Yosemite")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def get_elevation(self, xy):
        """
        Returns integer value of original data

        xy must be a tuple
        """
        return self.elevation_array[xy[0]][xy[1]]

    def get_norm_elevation(self, xy):
        """
        Returns integer value of normalized data

        xy must be a tuple
        """
        return self.norm_data_array[xy[0]][xy[1]]

    def get_slope(self, xy1, xy2):
        """
        Returns slope between two points

        xy1 and xy2 must be tuples
        """
        rise = self.get_elevation(xy1)-self.get_elevation(xy2)
        run = dist = np.linalg.norm(np.array(xy1)-np.array(xy2))
        return rise/run

    def normalize(self):
        """
        normalized data so the smallest data value is 0 and the largest is 255
        while maintaining the relative ratio of the rest of the data values
        """
        new_data_array = []
        temp_array = []
        OldMin = np.amin(self.elevation_array)
        OldMax = np.amax(self.elevation_array)
        NewMax = 255
        NewMin = 0

        for row in self.elevation_array:
            for val in row:
                new_val = int(np.round((((val - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin))
                temp_array.append(new_val)
            new_data_array.append(temp_array)
            temp_array = []

        return np.array(new_data_array)

map = elevation("US_DEM2016.tif")
map.display(1)
