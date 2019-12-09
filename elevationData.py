import gdal
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json


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

        temp = self.elevation_array.tolist()
        temp = temp[0:1110]
        for i in range(len(temp)):
            temp[i] = temp[i][0:1473]

        self.elevation_array = np.asarray(temp)


        self.norm_data_array = self.normalize()

    def display(self,resolution = 50):
        """
        Displays original data graphically
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
        """
        Displays normalized data graphically
        """
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
        e1 = self.get_elevation(xy1)
        e2 = self.get_elevation(xy2)
        rise = e1 - e2
        run = dist = np.linalg.norm(np.array(xy1)-np.array(xy2))*30
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

    def get_slope_list(self, xy):
        temp = []
        x = xy[0]
        y = xy[1]
        for cell in [(x-1,y+1),(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]:
            if (cell[0] < 0 or cell[1] < 0):
                temp.append(0.0)
                continue
            try:
                temp.append(self.get_slope(xy, cell))
            except IndexError:
                temp.append(0.0)

        return temp

    def cache(self):
        elevation_dict = {}
        norm_dict = {}
        slope_dict = {}
        for i in range(len(self.elevation_array)):
            for j in range(len(self.elevation_array[0])):
                elevation_dict[str((i,j))] = int(self.get_elevation((i,j)))
                norm_dict[str((i,j))] = int(self.get_norm_elevation((i,j)))
                slope_dict[str((i,j))] = self.get_slope_list((i,j))




        with open("elevation.json", 'w') as elevation_file:
            json.dump(elevation_dict, elevation_file)
        with open("norm_elevation.json", 'w') as norm_file:
            json.dump(norm_dict, norm_file)
        with open("slope.json", 'w') as slope_file:
            json.dump(slope_dict, slope_file)


map = elevation("US_DEM2016.tif")
map.cache()
