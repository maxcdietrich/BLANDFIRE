# BLANDFIRE

## Authors
Shawn Albertson, [Max Dietrich](https://github.com/maxcdietrich), Florian Michael-Schwarzinger

## Description
This code allows you to simulate a forest fire using python in a region of California, USA near Yosemite valley based on parameters including elevation profiles, wind speed and wind direction.

## Goal
We hope that this code can become a valuable tool for helping people in areas prone to forest fires predict the spread of these fires.

## Instructions

#### Packages
- GDAL
- Matplotlib
- numpy
- pygame
- eccodes

#### Installing numpy
Run `python -m pip install --user numpy` in the terminal

#### Installing Matplotlib
Run `python -m pip install -U matplotlib` from the terminal

#### Installing pygame
Run `python3 -m pip install -U pygame --user` from the terminal

#### Installing GDAL
Run `conda install GDAL` from the terminal

#### Installing eccodes
Visit [the installation page](https://confluence.ecmwf.int//display/ECC/ecCodes+installation) and follow the instructions as listed. Alternatively, the program can be downloaded using APT in the terminal using `sudo apt-get install python3-eccodes`

#### How to run the code
All .py files can be run from the terminal.

Once all data sets are downloaded (elevation.json, norm_elevation.json, final_shape.lcp, final_shape.prj, and [slope.json](https://drive.google.com/drive/folders/1ELMB5iuE5Ez03xmYkg5ZwO87WgNj3rbG?fbclid=IwAR35agd-1fEnZ1h9Ct4xXuKizvfS4fsl3oYCLMgz_0SgkGbWFik1fbL-Bw0)), then write_map.py can be run to create the data set used in the simulation, and then calculate_fire.py can be run to begin the simulation.  

**Large File Warning!**

write_map.py produces a file that is about 1.3 gigabytes.  Make sure there is space on your hard drive before running the program.

#### Quitting the Program
The program will automatically terminate if the fire is extinguished or if the iteration limit is reached.  By default this limit is 5000 iterations, however this can be changed in the final line of calculate_fire.py.  All programs can also be terminated by pressing ctrl+c in the terminal window running the program.

## Citations
- The wind data that we use in our model was generated with the [WindNinja](https://www.firelab.org/project/windninja) CFD tool.
- Elevation and fuel data was accessed through the [LANDFIRE](https://www.landfire.gov/index.php) database

## Contact Information
Shawn: salbertson@olin.edu<br />
Florian: fschwarzinger@olin.edu
