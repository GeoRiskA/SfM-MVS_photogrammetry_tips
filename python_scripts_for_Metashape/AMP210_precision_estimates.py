#-----------------------------------------------------------------------------------------------------------------
# Name:         AMP210_precision estimates.py
# Purpose:      Apply a Monte Carlo approach to estimate the precision of the
#               coordinates of the sparse point cloud (tie points) and camera
#               parameters.
#
# Compatibility: Agisoft Metashape Pro 2.0.x to 2.1.x
#
# Version 210 (Compatible with AMP 2.1.0) – 18 March 2024
#
# From the original work of Mike James (Lancaster University, UK)

# Citation:
# James, M.R., Robson, S., Smith, M.W., 2017.
# 3-D uncertainty-based topographic change detection with structure-from-motion
# photogrammetry: precision maps for ground control and directly georeferenced
# surveys.
# Earth Surface Processes and Landforms 42, 1769–1788
# https://doi.org/10.1002/esp.4125
#
# If used, please cite the above publication reference in your work!
#
# Maintained  and updated since v.140 by:
#     Benoît Smets
#     Royal Museum for Central Africa / Vrije Unversiteit Brussel (Belgium)
#
# With the support of:
#     - Silke Calcoen (MSc student, VUB/KULeuven, June 2023)
#     - Louise Delhaye (PhD researcher, VUB/RMCA, August 2020)
#
# Important Note:   Please follow the instructions here below!
#-----------------------------------------------------------------------------------------------------------------

# ORIGINAL DESCRIPTION OF THE SCRIPT:
# ===================================
#
# This script uses a Monte Carlo approach to enable precision estimates to be made for
# the coordinates of sparse points and camera parameters. Output files from the script can
# be processed using sfm_georef (http://tinyurl.com/sfmgeoref) and also provide variance-
# covariance information. Designed for use on projects containing a single chunk, with all photos 
# taken with the same camera.
#
# Precision estimates are made by carrying out repeated bundle adjustments ('optimisations' in Metashape)
# with different pseudo-random offsets applied to the image observations and the control measurements for each.
# The offsets are taken from normal distributions with standard deviations representative of the appropriate
# measurement precision within the survey, as given by the following Metashape settings:
#  Image coordinates:
# 		'Tie point accuracy'
# 		---> defines the image measurement precision for tie points (in pixels)
#		'Marker accuracy' (or 'Projection accuracy' in older versions)
#		---> defines the image measurement precision for markers (in pixels)
#
#  Measurement accuracy (i.e. survey precision of control measurements)
#		'Camera accuracy'
#		---> defines precision of known camera positions (can be set individually for each photo)
#		'Marker accuracy'
#		---> defines precision of ground control points positions (can be set individually for each marker)
#
# Estimated point precisions will not be correct unless the values of these settings have been appropriately 
# set within Metashape (e.g. 'tie point accuracy' should be set to the actual precision of the measurements
# as given by the RMS reprojection error in pixels - see James et al. 2017; doi: 10.1016/j.geomorph.2016.11.021).
# Note that use of camera angles or scalebars as control measurements have not been implemented in the script. The 
# script has only been used with Local or Projected coordinate systems (i.e. not with a GCS system). 
#
# INSTRUCTIONS TO USE THE SCRIPT:
# ===============================
#
# Requirements:   - The workspace must only contain one chunk
#                 - The workspace must be saved as a .psz file
#                 - The coordinate system(s) must be properly specified
#
# Usage:      1) Create of specific folder where to store the results of the precision estimate.
#             2) Open the script in a text editor and modify the hard-coded SETUP section according to the
#                processing you would like to perform. A good practice is to save the python script with a
#                personalised name, so you keep track of the parameters you selected for the precision
#                estimate.
#             3) Run the script. For this, go to the main menu bar and select "Tools > Run Script...".
#             4) Once finished, you only have the results of the iterations. You have to compute the statistics
#                out of that. To do so, you have to use SfM_georef (http://tinyurl.com/sfmgeoref). Please, read
#                the user guide of SfM_georef (Section 10, from p. 14) to properly perform the precision analysis.
#
# UPDATE LOG:
#============
# 18/04/24 Update of the header to make it more user friendly
# 15/06/23 Replaced "point_cloud" class by "tie_points", according to the new namings of version 2
#          Replaced "exportPoints" by "exportPointCloud"
#          Replaced "PointsFormatPLY" by "PointCloudFormatPLY"
#          Replaced "save_normals" by "save_point_normal"
#          Replaced "save_colors" by "save_point_color"
#          Replaced "PointCloudData" by "TiePointsData"
#          Under section "Reset the observations (projections) and add Gaussian noise - Markers": use of vector slicing to ensure equal vector dimensions 
# 27/08/20 Replaced saveReference() by exportReference()
#          Replaced parameters names in exportCameras(): Projection -> crs, rotation_order -> chan_rotation_order
# 21/08/20 Replaced parameters names in exportPoints(): normals -> save_normals; colors -> save_colors; Projection -> crs
#          Added "source_data=Metashape.PointCloudData" in "exportPoints" function
# 28/05/19 Replaced the 'PhotoScan' function by 'Metashape'
# 15/03/18 Added scalebars into the analysis
# 29/01/18 Removed fit_shutter for compatibility with v.1.4
# 28/01/18 Added export of initial sparse point cloud ('sparse_pts_reference.ply') for use as a reference in sfm_georef.
# 28/05/17 Fixed bug in calculation of observation distances, which only affected global relative precision estimates (ratios) made in sfm_georef.
# 25/02/17 Updated the camera parameter optimisation options to exploit the greater flexibility now offered.
# 25/02/17 Added a required test for non-None marker locations (PhotoScan now sets them to none if unselected). 
# 25/02/17 Multiple name changes to accommodate PhotoScan updates of chunk accuracy attributes (e.g. tie_point_accuracy).
# 25/02/17 Multiple changes to export function parameters to accommodate PhotoScan updates.
#-----------------------------------------------------------------------------------------------------------------

import Metashape
import random
import math
import csv
import os
NaN = float('NaN')

########################################################################################
######################################   SETUP    ######################################
########################################################################################
# Update the parameters below to tailor the script to your project.

# Directory where output will be stored and active control file is saved.
# Note use of '/' in the path (not '\'); end the path with '/'
# The files will be generated in a sub-folder named "Monte_Carlo_output"
# Change the path to the one you want, but there's no need to change act_ctrl_file.
dir_path = 'E:/PrecisionEstimates/'
act_ctrl_file = 'active_ctrl_indices.txt'

# Define how many times bundle adjustment (Metashape 'optimisation') will be carried out.
# 4000 used in original work, as a reasonable starting point.
num_randomisations = 5000

# Define the camera parameter set to optimise in the bundle adjustment.
# v.1.3 of Metashape enables individual selection/deselection of all parameters.
# Note - b1 was previously 'aspect ratio' (i.e. the difference between fx and fy)
#        b2 was previously 'skew'
optimise_f=True
optimise_cx=True
optimise_cy=True
optimise_b1=True
optimise_b2=True
optimise_k1=True
optimise_k2=True
optimise_k3=True
optimise_k4=False
optimise_p1=True
optimise_p2=True
optimise_p3=False
optimise_p4=False

# Points are exported as floats in binary ply files for speed and size, and thus cannot represent very small changes
# in large geographic coordinates. Thus, the offset below can be set to form a local origin and ensure numerical
# precision is not lost when coordinates are saved as floats. The offset will be subtracted from point coordinates.
# [RECOMMENDED] - Leave as NaN; the script will automatically calculate and apply a suitable offset, which will be saved
# as a text file for further processing, OR edit the line to impose a specific offset of your choice - 
# e.g.  pts_offset = Metashape.Vector( [266000, 4702000, 0] )
pts_offset = Metashape.Vector( [NaN, NaN, NaN] )

###################################   END OF SETUP   ###################################
########################################################################################

# Initialisation
chunk = Metashape.app.document.chunk
point_proj = chunk.tie_points.projections


# Need CoordinateSystem object, but PS only returns 'None' if an arbitrary coordinate system is being used
# thus need to set manually in this case; otherwise use the Chunk coordinate system.
if chunk.crs == None:
	crs = Metashape.CoordinateSystem('LOCAL_CS["Local CS",LOCAL_DATUM["Local Datum",0],UNIT["metre",1]]')
	chunk.crs = crs
else:
	crs = chunk.crs	

# Find which markers are enabled for use as control points in the bundle adjustment
act_marker_flags = []
for marker in chunk.markers:
	act_marker_flags.append(marker.reference.enabled)
num_act_markers = sum(act_marker_flags)

# Write the active marker flags to a text file - one line per BA iteration
# This is actually relict code and not strictly needed.		
with open(dir_path + act_ctrl_file, 'w') as f:
	fwriter = csv.writer(f, delimiter=' ', lineterminator='\n')
	for line_ID in range(0, num_randomisations):
		fwriter.writerow( [int(elem) for elem in act_marker_flags] ) 
	f.close()
	
# Find which camera orientations are enabled for use as control in the bundle adjustment
act_cam_orient_flags = []
for cam in chunk.cameras:
	act_cam_orient_flags.append(cam.reference.enabled)
num_act_cam_orients = sum(act_cam_orient_flags)

# Reset the random seed, so that all equivalent runs of this script are started identically
random.seed(1)

# Carry out an initial bundle adjustment to ensure that everything subsequent has a consistent reference starting point.
chunk.optimizeCameras(fit_f=optimise_f, fit_cx=optimise_cx, fit_cy=optimise_cy, fit_b1=optimise_b1, fit_b2=optimise_b2, fit_k1=optimise_k1, fit_k2=optimise_k2, fit_k3=optimise_k3, fit_k4=optimise_k4, fit_p1=optimise_p1, fit_p2=optimise_p2, fit_p3=optimise_p3, fit_p4=optimise_p4)

# If required, calculate the mean point coordinate to use as an offset
if math.isnan(pts_offset[0]):
	points = chunk.tie_points.points
	npoints = 0
	pts_offset = Metashape.Vector( [0, 0, 0] )
	for point in points:
		if not point.valid:
			continue
		npoints += 1
		pts_offset[0] += point.coord[0]
		pts_offset[1] += point.coord[1]
		pts_offset[2] += point.coord[2]
	
	pts_offset = crs.project(chunk.transform.matrix.mulp(pts_offset/npoints))
	pts_offset[0] = round(pts_offset[0], -2)
	pts_offset[1] = round(pts_offset[1], -2)
	pts_offset[2] = round(pts_offset[2], -2)
	
# Save the used offset to text file
with open(dir_path + '_coordinate_local_origin.txt', "w") as f:
	fwriter = csv.writer(f, dialect='excel-tab', lineterminator='\n')
	fwriter.writerow( pts_offset )
	f.close()

# Export a text file of observation distances and ground dimensions of pixels from which relative precisions can be calculated
# File will have one row for each observation, and three columns:
# cameraID      ground pixel dimension (m)   observation distance (m)
points = chunk.tie_points.points
npoints = len(points)
camera_index = 0
with open(dir_path + '_observation_distances.txt', "w") as f:
	fwriter = csv.writer(f, dialect='excel-tab', lineterminator='\n')
	for camera in chunk.cameras:
		camera_index += 1
		if not camera.transform:
			continue
			
		# Accommodate change in attribute name in v.1.2.5
		try:
			fx = camera.sensor.calibration.fx
		except AttributeError:
			fx = camera.sensor.calibration.f
		
		point_index = 0
		for proj in chunk.tie_points.projections[camera]:
			track_id = proj.track_id
			while point_index < npoints and points[point_index].track_id < track_id:
				point_index += 1
			if point_index < npoints and points[point_index].track_id == track_id:
				if not points[point_index].valid:
					continue
				dist = (chunk.transform.matrix.mulp(camera.center) - chunk.transform.matrix.mulp(Metashape.Vector( [points[point_index].coord[0], points[point_index].coord[1], points[point_index].coord[2]]))).norm()
				fwriter.writerow( [camera_index, '{0:.4f}'.format(dist/fx), '{0:.2f}'.format(dist)] )

	f.close()

# Export a text file with the coordinate system
with open(dir_path + '_coordinate_system.txt', "w") as f:
	fwriter = csv.writer(f, dialect='excel-tab', lineterminator='\n')
	fwriter.writerow( [crs] )
	f.close()
	
# Make a copy of the chunk to use as a zero-error reference chunk
original_chunk = chunk.copy()
	
# Set the original_marker locations be zero error, from which we can add simulated error
for original_marker in original_chunk.markers:
	if original_marker.position is not None:
		original_marker.reference.location = crs.project(original_chunk.transform.matrix.mulp(original_marker.position))
	  
# Set the original_marker and point projections to be zero error, from which we can add simulated error
original_points = original_chunk.tie_points.points
original_point_proj = original_chunk.tie_points.projections
npoints = len(original_points)
for camera in original_chunk.cameras:
	if not camera.transform:
		continue
		
	point_index = 0
	for original_proj in original_point_proj[camera]:
		track_id = original_proj.track_id
		while point_index < npoints and original_points[point_index].track_id < track_id:
			point_index += 1
		if point_index < npoints and original_points[point_index].track_id == track_id:
			if not original_points[point_index].valid:
				continue
			original_proj.coord = camera.project(original_points[point_index].coord)

	# Set the original marker points be zero error, from which we can add simulated error
	# Note, need to set from chunk because original_marker.position will be continuously updated
	for markerIDx, original_marker in enumerate(original_chunk.markers):
		if (not original_marker.projections[camera]) or (not chunk.markers[markerIDx].position):
			continue
		original_marker.projections[camera].coord = camera.project(chunk.markers[markerIDx].position)
		
# Export this 'zero error' marker data to file
original_chunk.exportMarkers(dir_path + 'referenceMarkers.xml')

# Derive x and y components for image measurement precisions
tie_proj_x_stdev = chunk.tiepoint_accuracy / math.sqrt(2)
tie_proj_y_stdev = chunk.tiepoint_accuracy / math.sqrt(2)
marker_proj_x_stdev = chunk.marker_projection_accuracy / math.sqrt(2)
marker_proj_y_stdev = chunk.marker_projection_accuracy / math.sqrt(2)

# Carry out an adjustment with a fixed camera to define a benchmark set of sparse points for later comparison.
# Ideally, this should be the same as the sparse points in the zero-error chunk, but there do seem to be some differences.
# Make a copy of the zero-error reference chunk to run the adjustment on
temp_chunk = original_chunk.copy()

# Carry out a bundle adjustment with a fixed camera model.
temp_chunk.optimizeCameras(fit_f=False, fit_cx=False, fit_cy=False, fit_b1=False, fit_b2=False, fit_k1=False, fit_k2=False, fit_k3=False, fit_k4=False, fit_p1=False, fit_p2=False, fit_p3=False, fit_p4=False)
 
# Export the sparse point cloud 
temp_chunk.exportPointCloud(dir_path + 'sparse_pts_reference.ply', source_data=Metashape.TiePointsData, save_point_normal=False, save_point_color=False, format=Metashape.PointCloudFormatPLY, crs=crs, shift=pts_offset)			

# Delete this chunk
Metashape.app.document.remove([temp_chunk])

# Counter for the number of bundle adjustments carried out, to prepend to files
file_idx = 1  	
Metashape.app.document.chunk = chunk

# Make the ouput directory if it doesn't exist
dir_path = dir_path + 'Monte_Carlo_output/'
os.makedirs(dir_path, exist_ok=True)

########################################################################################
# Main set of nested loops which control the repeated bundle adjustment
for line_ID in range(0, num_randomisations ):
	# Reset the camera coordinates if they are used for georeferencing
	if num_act_cam_orients > 0:
		for camIDx, cam in enumerate(chunk.cameras):
			if not cam.reference.accuracy:
				cam.reference.location = ( original_chunk.cameras[camIDx].reference.location +
				Metashape.Vector( [random.gauss(0, chunk.camera_location_accuracy[0]), random.gauss(0, chunk.camera_location_accuracy[1]), random.gauss(0, chunk.camera_location_accuracy[2])] ) )
			else:
				cam.reference.location = ( original_chunk.cameras[camIDx].reference.location +
				Metashape.Vector( [random.gauss(0, cam.reference.accuracy[0]), random.gauss(0, cam.reference.accuracy[1]), random.gauss(0, cam.reference.accuracy[2])] ) )

	# Reset the marker coordinates and add noise
	for markerIDx, marker in enumerate(chunk.markers):
		if not marker.reference.accuracy:
			marker.reference.location = ( original_chunk.markers[markerIDx].reference.location +
			Metashape.Vector( [random.gauss(0, chunk.marker_location_accuracy[0]), random.gauss(0, chunk.marker_location_accuracy[1]), random.gauss(0, chunk.marker_location_accuracy[2])] ) )
		else:
			marker.reference.location = ( original_chunk.markers[markerIDx].reference.location +
			Metashape.Vector( [random.gauss(0, marker.reference.accuracy[0]), random.gauss(0, marker.reference.accuracy[1]), random.gauss(0, marker.reference.accuracy[2])] ) )

	# Reset the scalebar lengths and add noise
	for scalebarIDx, scalebar in enumerate(chunk.scalebars):
		if scalebar.reference.distance:
			if not scalebar.reference.accuracy:
				scalebar.reference.distance = ( original_chunk.scalebars[scalebarIDx].reference.distance +
				random.gauss(0, chunk.scalebar_accuracy) )
			else:
				scalebar.reference.distance = ( original_chunk.scalebars[scalebarIDx].reference.distance +
				random.gauss(0, scalebar.reference.accuracy) )
				
	# Reset the observations (projections) and add Gaussian noise
	for photoIDx, camera in enumerate(chunk.cameras):
		original_camera = original_chunk.cameras[photoIDx]	
		if not camera.transform:
			continue
		
		# Tie points (matches)
		matches = point_proj[camera]
		original_matches = original_point_proj[original_camera]
		for matchIDx in range(0, len(matches)):	
			matches[matchIDx].coord = ( original_matches[matchIDx].coord + 
			Metashape.Vector( [random.gauss(0, tie_proj_x_stdev), random.gauss(0, tie_proj_y_stdev)] ) )
            
      # Markers
		for markerIDx, marker in enumerate(chunk.markers):
			if not marker.projections[camera]:
				continue
			print('Added noise dimensions: ' + str(Metashape.Vector([random.gauss(0, marker_proj_x_stdev), random.gauss(0, marker_proj_y_stdev)]).size), 'Marker projection coordinates dimensions: ' + str(original_chunk.markers[markerIDx].projections[original_camera].coord[0:2].size))
			marker.projections[camera].coord = ( original_chunk.markers[markerIDx].projections[original_camera].coord[0:2] +	Metashape.Vector([random.gauss(0, marker_proj_x_stdev), random.gauss(0, marker_proj_y_stdev)]) )    
	
    
	# Construct the output file names
	out_file = ('{0:04d}'.format(file_idx) + '_MA' + '{0:0.5f}'.format(chunk.marker_location_accuracy[0]) + 
	'_PA' + '{0:0.5f}'.format(chunk.marker_projection_accuracy) + '_TA' + '{0:0.5f}'.format(chunk.tiepoint_accuracy)+ 
	'_NAM' + '{0:03d}'.format(num_act_markers) + '_LID' + '{0:03d}'.format(line_ID+1) )
	out_gc_file = out_file + '_GC.txt'
	out_cams_c_file = out_file + '_cams_c.txt'
	out_cam_file = out_file + '_cams.xml'
	print( out_gc_file )
	
	# Bundle adjustment
	chunk.optimizeCameras(fit_f=optimise_f, fit_cx=optimise_cx, fit_cy=optimise_cy, fit_b1=optimise_b1, fit_b2=optimise_b2, fit_k1=optimise_k1, fit_k2=optimise_k2, fit_k3=optimise_k3, fit_k4=optimise_k4, fit_p1=optimise_p1, fit_p2=optimise_p2, fit_p3=optimise_p3, fit_p4=optimise_p4)

	# Export the control (catch and deal with legacy syntax)
	try:
		chunk.exportReference(dir_path + out_gc_file, Metashape.ReferenceFormatCSV, items=Metashape.ReferenceItemsMarkers,)
		chunk.exportReference(dir_path + out_cams_c_file, Metashape.ReferenceFormatCSV, items=Metashape.ReferenceItemsCameras)
	except:
		chunk.exportReference(dir_path + out_gc_file, 'csv')
		
	# Export the cameras
	chunk.exportCameras(dir_path + out_cam_file, format=Metashape.CamerasFormatXML, crs=crs, chan_rotation_order=Metashape.RotationOrderXYZ)
	
	# Export the calibrations [NOTE - only one camera implemented in export here]
	for sensorIDx, sensor in enumerate(chunk.sensors):
		sensor.calibration.save(dir_path + out_file + '_cal' + '{0:01d}'.format(sensorIDx+1) + '.xml')

	
	# Export the sparse point cloud
	chunk.exportPointCloud(dir_path + out_file + '_pts.ply', source_data=Metashape.TiePointsData, save_point_normal=False, save_point_color=False, format=Metashape.PointCloudFormatPLY, crs=crs, shift=pts_offset)			
	
	# Increment the file counter
	file_idx = file_idx+1

# Metashape.app.document.remove([original_chunk])

#-------------------------------------------------------------------------------
#     END OF CODE
