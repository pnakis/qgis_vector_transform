Author: Nakis Panagiotis<br />
Email : pnakis@hotmail.com<br />
Date : June 2017<br />
Repository: https://github.com/pnakis/qgis_vector_transform<br />
Tools used: Plugin Builder by GeoApt LLC<br />
            Qt Designer by The Qt Company<br />

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

Transformations included in the plygin: 
1) Translation 

x' = x + Tx<br />
y' = y + Tx<br />

2) Rotation 

x' = cos(rx)*x + sin(ry)*y<br />
y' = -sin(rx)*x + cos(ry)*y<br />

3) Scale

x' = x*sx<br />
y' = y*sy<br />

4) Similarity

x' = cos(r)*s*x + sin(r)*s*y + Tx<br />
y' = -sin(r)*s*x + cos(r)*s*y + Ty<br />

5) Affine 

a = sx*(cos(r) + d*sin(r))<br />
b = sy*sin(r)<br />
c = sx*(-sin(r) + d*cos(r))<br />
d = sy*cos(r)<br />

x' = a*x + b*y + Tx<br />
y' = c*x + d*y + Ty<br />

6) Affine (with known coefficients)

x' = a1*x + b1*y + c1<br />
y' = a2*x + b2*y + c2<br />

7) Projective

x' = (a1*x + b1*y + c1) / (a0*x + b0*y + 1)<br />
y' = (a2*x + b2*y + c2) / (a0*x + b0*y + 1)<br />

where:
x',y' are the new and <br />
x,y are the input coordinates<br />
Tx, Ty are the axis translation parameters<br />
sx, sy are the axis scale parameters and <br />
s the global scale parameter<br />
rx, ry are the axis rotation parameters and<br />
r the global rotation parameter<br />
delta is the axis perpenticularity parameter<br />
