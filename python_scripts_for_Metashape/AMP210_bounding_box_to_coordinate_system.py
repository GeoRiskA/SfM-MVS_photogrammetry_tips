#-------------------------------------------------------------------------------
# Name:         AMP210_bounding_box_to_coordinate_system.py
# Purpose:      Rotates model bounding box to fit the coordinate system. The
#               bounding box size is kept.
#
# Compatibility: Agisoft Metashape Pro 1.5.x to 2.1.x
#
# Version 210 (Compatible with AMP 2.1.0) – 18 March 2024
#
# Author from version 150:
#     Benoît Smets
#     Royal Museum for Central Africa / Vrije Unversiteit Brussel (Belgium)
#
# Previous authors:
# Author version PS110: James Dietrich, Dartmouth College, 2015
# Author version PS090: Agisoft Support Staff, 2013
#
# Usage:            Open the script file in Metashape Pro
#                   --> In the main menu bar: Tools > Run Scripts...
#
# Important Note:   The coordinate system of the project needs to be set to
#                   something else than 'Local Coordinates'
#-------------------------------------------------------------------------------

import Metashape
import math

doc = Metashape.app.document

chnk = doc.chunk

T = chnk.transform

v = Metashape.Vector( [0,0,0,1] )

v_t = T.matrix * v

v_t.size = 3

m = chnk.crs.localframe(v_t)

m = m * T.matrix

s = math.sqrt(m[0,0]*m[0,0] + m[0,1]*m[0,1] + m[0,2]*m[0,2]) #scale factor

R = Metashape.Matrix( [[m[0,0],m[0,1],m[0,2]], [m[1,0],m[1,1],m[1,2]], [m[2,0],m[2,1],m[2,2]]])

R = R * (1. / s)

reg = chnk.region
reg.rot = R.t()
chnk.region = reg

#-------------------------------------------------------------------------------
#     END OF CODE