import gdal
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

filename = "map.tif"
gdal_data = gdal.Open(filename)
gdal_band = gdal_data.GetRasterBand(1)
nodataval = gdal_band.GetNoDataValue()

data_array = gdal_data.ReadAsArray().astype(np.float)
data_array

if np.any(data_array == nodataval):
    data_array[data_array == nodataval] = np.nan

fig = plt.figure(figsize = (12, 12))
ax = fig.add_subplot(111)
plt.contourf(data_array, cmap = "viridis",
            levels = list(range(5000)))
plt.title("Yosemite")
cbar = plt.colorbar()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
