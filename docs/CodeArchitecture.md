# Code Architecture

Our simulation begins with raw GIS data for wind and elevation.  These were gathered manually with [WindNinja](https://www.firelab.org/project/windninja), and [LANDFIRE](https://www.landfire.gov/index.php) respectively.  These data files were then processed into data sets that our model could understand and exported either as lists of values, or JSON files mapping values to (x,y) coordinate pairs.  Our next step was to combine these disparate data streams into a cohesive unit.  This took the form of a large JSON file mapping all of the data we needed to every coordinate pair in our simulation.  The resulting "map" is read by our rendering and modelling functions to generate animations of the fire spreading

##### [Return Home](index.html)
