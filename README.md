# SfM-MVS photogrammetry tips
-------------

**This repository provides useful explanations, references, links and scripts to help you perform Structure-from-Motion Mutli-View Stereo (SfM-MVS) photogrammetry with the software [Agisoft Metashape Pro](https://www.agisoft.com/).**  

This repository is still in construction. The information currently available is limited to a first version of a user guide and few Python scripts to perform specific processing steps with Metashape Pro.

## TABLE OF CONTENT  

1. Metashape Pro user guide
2. Python scripts for Metashape Pro
3. Useful shell scripts to manage or pre-process (UAV) imagery
4. *Video tutorials (not available yet)*

----------

## 1. Metashape Pro user guide

Agisoft Metashape Pro (AMP) is amongst the best SfM-MVS photogrammetry software in the market. Although expensive (~3500$ for the pro version), there is a more effordable price for researchers with the Educational Licence (~550$). Each new version of the software comes with new tools and options, but the main workflow remains the same. In the user guide proposed here, in markdown format, you will find a description on how to process of set of images to create a dense point cloud, a digital elevation model (DEM) and an orthomosaic, using this main workflow.  

The user guide is progressively updated with additional tips and figures to make it more detailed and easy to use. However, the optional processing steps that could be done (e.g., image colour correction) or the post-processing and analysis tools (e.g., point cloud classification) are not detailed here. These options might be described in the future through tutorials.  

Currently, the most recent version of the tutorial is [version 1.0.0](https://github.com/GeoRiskA/SfM-MVS_photogrammetry_tips/blob/main/User_Guide_v100.md)  


----------

## 2. Python scripts for Metashape Pro

In the folder [python_scripts_for_Metashape](https://github.com/GeoRiskA/SfM-MVS_photogrammetry_tips/tree/main/python_scripts_for_Metashape), you will find a series of Python scripts used to perform additional processing on your photogrammetric results or automate specific actions.   

The scripts currently available are:  

- **AMP210_Chunk_Duplicator.py:** Script to duplicate as many times as you want one of the chunks of you Metashape Pro project. Before using it, you must modify the script to specify 1) the name of the chunk, and 2) the number of times you would like to duplicate the chunk. *[Compatible with Metashape Pro version 2.1 and above]*

- **AMP210_bounding_box_to_coordinate_system.py:** Script to align the "region" (bounding box surrounding the point clouds) with the coordinate system. No previous hard-coding in the script is necessary. This script is really important and should be used before creating a digital elevation model or an orthomosaic. *[Compatible with Metashape Pro version 1.5 and above]*

- **AMP210_precision_estimates.py:** Script initially created by [James et al. (2017)](https://doi.org/10.1016/j.geomorph.2016.11.021) for the versions 1.3 and 1.4 of Metashape Pro (formerly Photoscan Pro), and updated to be used with more recent versions of the software. This script is used to estimate the precision of the 3D photogrammetric reconstruction using a Monte-Carlo statistical approach. A setup section must be modified in the script before its use. Once the results are obtained, the software [SfM-georef](http://tinyurl.com/sfmgeoref) developed by [Mike James](https://www.lancaster.ac.uk/staff/jamesm/home.htm) must be used to obtain the precision estimate. More information on how to use this script and SfM-georef is [available here](https://www.lancaster.ac.uk/staff/jamesm/software/sfm_georef.htm). *[Compatible with Metashape Pro version 2.0 and above]*   

Other Python scripts for Metashape Pro are directly available on [the GitHub account of Agisoft](https://github.com/agisoft-llc/metashape-scripts). Here is a selection of useful scripts (currently only one) with the link to the repository of Agisoft:   

- **Split in Chunks:** Script that takes your chunk and split it into tiles, based on a user-defined grid (number columns and rows). Additional options are also available, such as performing the dense matching for each tile of the grid, and merging the results back into a single chunk. The script is classically launched using `Tools > Run Script...`. This action opens a new graphical user interface (GUI) in which the parameters and options can be selected by the user. [--> LINK](https://github.com/agisoft-llc/metashape-scripts/blob/master/src/split_in_chunks_dialog.py)  


----------

## 3. Useful shell scripts to manage or pre-process (UAV) imagery

In progress...

----------

## 4. Video tutorials

In progress...

----------
***(c) Benoît Smets, Royal Museum for Central Africa / Vrije Universiteit Brussel, 2023-2024***  
