Author: Nakis Panagiotis
Email : pnakis@hotmail.com
Date : June 2017
Repository: https://github.com/pnakis/qgis_vector_transform
Tools used: Plugin Builder by GeoApt LLC
            Qt Designer by The Qt Company

LICENSE:
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

INSTALLATION:
Place the entire folder VectorTransformation inside the directory:

C:\Users\{Your Username}\.qgis2\python\plugins\

and load the plugin for the QGIS program:

Plugins > Installed > Vector Transformation


ABOUT:
This plugin was created during my Masters Programme at the Technological Educational Institute of Athens,
department of Surveying & Geoinformatics Engineering with the title "Geospatial Technologies" for the 
course "Programming & Geospatial Applications".

This plugin applies transformations on vector layers and saves the new geometry in a new shapefile along with the old layer attributes.
It supports layer geometry types of: Points, MultiPoits, Lines, MultiLines, Polygons and MultiPolygons.

USAGE:
1) Load Layers in QGIS
2) Run the plugin
3) Choose transformation from the list
4) Enter variables
5) Select output shapefile location (DO NOT OVERWRITE EXISTING SHAPEFILE)
6) Press OK to run the module

Transformation included in the plygin: 
1) Translation 

x' = x + Tx
y' = y + Tx

2) Rotation 

x' = cos(rx)*x + sin(ry)*y
y' = -sin(rx)*x + cos(ry)*y

3) Scale

x' = x*sx
y' = y*sy

4) Similarity

x' = cos(r)*s*x + sin(r)*s*y + Tx
y' = -sin(r)*s*x + cos(r)*s*y + Ty

5) Affine 

a = sx*(cos(r) + d*sin(r))
b = sy*sin(r)
c = sx*(-sin(r) + d*cos(r))
d = sy*cos(r)

x' = a*x + b*y + Tx
y' = c*x + d*y + Ty

6) Affine (with known coefficients)

x' = a1*x + b1*y + c1
y' = a2*x + b2*y + c2

7) Projective

x' = (a1*x + b1*y + c1) / (a0*x + b0*y + 1)
y' = (a2*x + b2*y + c2) / (a0*x + b0*y + 1)

where:
x',y' are the new and 
x,y are the input coordinates
Tx, Ty are the axis translation parameters
sx, sy are the axis scale parameters and 
s the global scale parameter
rx, ry are the axis rotation parameters and
r the global rotation parameter
delta is the axis perpenticularity parameter
