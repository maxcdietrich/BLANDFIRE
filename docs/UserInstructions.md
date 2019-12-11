# Instructions

## Packages
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

#### Installing pyshp
Run `pip install pyshp` from the terminal

## Collecting data

### Wind Data
Acquiring detailed wind data is crucial for the representation of wildfire. WindNinja is a lightweight simulation tool which is made to study air flow over topographic regions.

#### Installing WindNinja on Linux
Visit https://github.com/firelab/windninja/wiki/Building-WindNinja-on-Linux for instructions on building WindNinja using CMake.

#### Installing WindNinja on Windows
https://www.firelab.org/document/windninja-software

### Topographic data
Visit https://www.landfire.gov/getdata.php and follow prompts to Data Distribution site. This tool allows you to download data for a specified region.

## How to run the code
All .py files can be run from the terminal.

Once all data sets are downloaded (elevation.json, norm_elevation.json, final_shape.lcp, final_shape.prj, and [slope.json](https://drive.google.com/drive/folders/1ELMB5iuE5Ez03xmYkg5ZwO87WgNj3rbG?fbclid=IwAR35agd-1fEnZ1h9Ct4xXuKizvfS4fsl3oYCLMgz_0SgkGbWFik1fbL-Bw0)), then write_map.py can be run to create the data set used in the simulation, and then calculate_fire.py can be run to begin the simulation.  

**Large File Warning!**

write_map.py produces a file that is about 1.3 gigabytes.  Make sure there is space on your hard drive before running the program.

## Quitting the Program
The program will automatically terminate if the fire is extinguished or if the iteration limit is reached.  By default this limit is 5000 iterations, however this can be changed in the final line of calculate_fire.py.  All programs can also be terminated by pressing ctrl+c in the terminal window running the program.



##### [Return Home](index.html)
