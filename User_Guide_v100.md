# Photogrammetric processing with Metashape Pro - A user guide

*(c) Benoît SMETS — Vrije Universiteit Brussel / Royal Museum for Central Africa*  
*Version 1.0 — 28 March 2023*   
#SfM-MVS #photogrammetry #Agisoft #Metashape #userguide

---------

This user guide aims at summarising the procedure to perform a proper photogrammetric processing of photographs acquired with a digital camera, using the <a href="https://www.agisoft.com/">Agisoft Metashape Pro software</a>, for topographic reconstruction and/or orthorectified ground surface imaging. A similar workflow is applicable for the 3D modelling of objects, but specificities of such kind of photogrammetric processing are not covered here. If your purpose is to process scanned aerial photographs (with fiducial marks) or satellite images for 3D photogrammetric reconstruction, the explanations proposed in this guide are not appropriate. Other user guides will soon be proposed for these purposes.  

In the present guide, it is assumed that the user already knows the fundamentals of Structure-from-Motion Multi-View Stereo (SfM-MVS) photogrammetry. Explanations will only focus on how to use Agisoft Metashape Pro to preform this type of processing.  

As a final introductory word, I strongly suggest you to, first, read the <a href="https://www.agisoft.com/downloads/user-manuals/">user manual provided by Agisoft</a>, or at least to have it with you while going through this guide.  

<br>

## Preliminary conditions

Nowadays, digital image acquisition is the most important step in SfM-MVS photogrammetry. Photogrammetry is a well established measurement method, with base equations developed during the 19th and 20th centuries. All available modern software programs can provide results of similar quality, as long as the imaging survey was performed in appropriate conditions, with the required equipment.  

Hence, it is considered here that the image acquisition has been performed properly, with these key considerations taken into account:  

- *Good camera and lens (preferably fixed lens), with identical focal length between photo shots.*
- *Sharp and properly exposed photos.*
- *Important overlap (i.e., 70 to 90 %) between the photos, along- and across-track.*
- *Point of views sub-perpendicular to the main planes of the targeted surface.*
- *Convergent views, at least as a complement to the main image dataset.*
- If needed and/or possible, ground control points (GCPs) or coded targets homogenously distributed in the area of interest. Direct georeferencing (i.e., precise positionning of photo shots) is another alternative.  

<br>

## Main Graphical User Interface (GUI)


Figures 1 and 2 show the main GUI of Metashape pro, with the location of the main menus, toolbars and tabs. These figures help to understand the procedures described in this user guide.


<img src="https://github.com/GeoRiskA/SfM-MVS_photogrammetry_tips/blob/main/Figures/AMP_GUI1_labeled.png" width=600>
<p><b>Figure 1 — Main Graphical User Interface (GUI) of Metashape Pro (Part 1)</b></p>    
   
<img src="https://github.com/GeoRiskA/SfM-MVS_photogrammetry_tips/blob/main/Figures/AMP_GUI2_labeled.png" width=600>
<p><b>Figure 2 — Main Graphical User Interface (GUI) of Metashape Pro (Part 2)</b></p>    


## 1. Image preparation


#### 1.1. Image pre-processing

Image pre-processing may be required for your dataset, before doing any kind of photogrammetric processing. This especially the case when the photos were shot in RAW format. In any case, the image pre-processing must provide an optimal result for image matching, while avoiding contrast and tone differences between photographs, which would lead to colour variations in the final orthomosaic. The key aspects to take into account during this pre-processing:  

- Avoid under- and over-exposure
- Correct any vignetting or chromatic abberration visible in the imagery
- If illumination varied significantly during the photo acquisition, homogenise the contrast and tone using, e.g., histogram matching
- Avoid image compression as much as possible
- If useful, increase image sharpness through a sharpening processing

#### 1.2. Image import

To import images in Metashape Pro, open the software, go to `Workflow > Add Photos...` and select the photos you would like to use. The photos will appear in a "Chunk" of the Workspace, which corresponds to a processing job in which you will have all your input data and all the results of your processing. Once imported, the folder "Cameras" in the chunk will display the list of the photos and will specify between brackets that none of the photos are aligned.  

The first reflex to have is to check that the software properly recognises the type of images you have imported. To do so, go to `Tools > Camera Calibration...` and look at the following parameters derived from the image metadata:  
- The camera group (left column) recognizes the camera model
- The camera type is set to "Frame" (corresponds to most of the cameras you will use)
- The pixel size is specified
- The focal length is correct

#### 1.3. Image quality

Once you are sure that the photos are properly recognised by the software, the first processing step is to check the quality (i.e., sharpness and texture) of the photos. For this, Metashape Pro has an excellent tool that allows you to assess the image quality and eventually remove less good images.  

Right-click on an image of the dataset, either in the chunk or in the "Photos" frame, and select `Estimate Image Quality...`. A small window entitled "Analyze Photos" will appear. In the "Apply to" section, select "All cameras" and click "OK". In the "Photos" frame, the column entitled "Quality" will now be filled with decimal values ranging from 0 (useless photo) to 1 (photo of perfect quality).  

It is good practice to remove photos having a quality value lower than 0.7. You can be more severe if images have an overall better quality and that only few photos are removed. Use a lower quality value threshold only if removing photos with a quality lower than 0.7 significantly affects the image overlap and, hence, the 3D reconstruction.  

<br>

## 2. Photo alignment

You are now ready to start the photogrammetric processing. The first step is to detect remarkable points, called **"key points"** in the images, and find similar key points, called **"tie points"**, in image pairs. This two-step processing (i.e., key point detection and image matching) is called **"photo alignment"** in Metashape Pro. In this processing step, the interior and exterior orientations are calculated thanks to the tie points.

***Important note:*** *During a first installation of Metashape Pro, the most recent installers tend to disable a useful option allowing you to save the key points detected on the images. This option is mandatory to allow co-alignment. To enable this option, go to* `Tools > Preferences...` *(Windows) or* `MetashapePro > Preferences...` *(MacOS), and select the "Advanced" Tab. Finally, enable "Keep key points" (first option in the list).*  

To perform the photo alignment, first go to `Workflow > Align Photos...`. A small window will open. In the "General" section set the accuracy to "Highest". Reduce to "High" or "Medium" if your dataset is of poor quality or if you cannot properly align all the images.  

In the "Advanced" section, adapt the "key point limit per megapixel" if necessary. A value between **40,000** and **100,000** is usually enough, but higher values sometimes improve the results. To choose this value, you can run several times the photo alignment and check if you always reach this maximum key point value per photo or not. If this is the case, you may increase the value. For the "tie point limit", the most convenient choice is to set it to **0**, which means that there is no limit. Such a setting will of course lead to a longer processing time, but it usually provides the best results. The options "Exclude stationary tie points", "Guided image matching" and "Adaptive camera model fitting" can be selected.  

Once the processing is finished, you will end up with a "Sparse Point Cloud (SPC)"corresponding to the reprojection of the tie points in an arbitrary 3D space. If the images are geotagged, the software will automatically set the coordinate system into a geographic one (usually, lat/long coordinates, with the WGS84 datum). Point colour is derived from the photos and already allow you to see the ground surface and objects (vegetation, buildings, etc.) in 3 dimensions. In the `Model > Show/Hide Items` menu, you can display or hide the position of the camera, the bounding box surrounding the 3D reconstruction (called "Region"), the trackball, the ground control points (called "markers"), etc.  

To see the quality of the tie point positonning, it is possible to calculate a variance and, then, see which points are best reprojected in 3D. To do so, go to the reference tab (see lower left tab selection), click on the star symbol ("Optimize Cameras") and, in the newly opened window, select the two options: "Adaptive camera model fitting" and "Estimate tie point covariance". Once done, in the toolbar menu, on the top of the main window, click on the small arrow next to the "Point cloud" icon and choose "Point Cloud Variance" to replace the RGB colour of the points with a colour scale indicating the calculated variance. Points are now vectors with a length proportional to the variance. As long as tie points appear as points, and not lines, the variance is sufficiently good. Long and red vectors should be removed to improve the calculation of interior and exterior orientations. This filtering will be performed in Section 4.  
<br>

## 3. Georeferencing


The georeferencing of the 3D reconstruction can be performed in 2 ways: (1) using geotagged photos, or (2) using ground control points (GCPs). If there is no georeferencing information available, a solution is to use a reference dataset and co-align the data to it (approach not described here).

The first approach is straightforward and performed automatically by the software, if it is able to properly read the image metadata. This georeferencing methods is accurate when the two following conditions are met:
- The image positions are homogenously distributed in space, both horizontally and vertically. Having image acquisitions solely in a same plane will significantly decrease the georeferencing precision in the dimension perpendicular to the image acquisition plane.
- The camera position is accurate thanks to a positionning performed with a differential GNSS method, either in real-time (i.e., Real-Time Kinematic or "RTK") or in post-processing (i.e., Post-Processing Kinematic or "PPK").

The second approach requires the measurement of GCPs (markers) on the field, using a proper geodetic equipment (i.e., differential GNSS or EDM). The same conditions for accurate georeferencing apply:  
- The GCPs are homogeneously distributed within and ideally around the region of interest.
- The position of the GCPs was measured using a differential GNSS equipment.

When the geotagging of the images is used for the georeferencing, the coordinates of the photos can be observed in the camera geolocation frame (Fig. 2). The mean camera position error (in metres) is visible in bold, below the column "Error (m)". This error represents the variability between the camera positions when used for georeferencing. It does not represent the mean accuracy of measurement of each camera position, which is rather around 10 metres without differential correction and few centimetres to decimetres with differential correction.  

When GCPs are used for the georeferencing, their name and coordinates can be inserted, either manually or automatically using `File > Import > Import Markers...`. In both cases, their position in the images must be set manually on each image showing the GCP. This is why there are two types of accuracy to specify in reference settings: "Measurement accuracy" (= GCP position measurement in the field) and "image coordinate accuracy" (= GCP position in the images). Measurement accuracy will be expressed in metres. Image coordinate accuracy will be expressed in pixels. The default values must be adapted according to the quality of your georeferencing data.

Before applying the georeferencing, there are two steps to perform:  

(1) Make sure that you selected the proper coordinate system(s) in Reference Settings: Go to the Reference frame (Fig. 2) and select the "Settings" symbol (tools icon). Specify the correct coordinate system. If the coordinates of the photos or those of the GCPs (markers) are different from the final coordinate system you would like to use, you can specify it in these settings. Adapt the accuracy values and click "OK" to validate.  

(2) Make sure you selected the images and GCPs you would like to use for georeferencing. Unticked images and GCPs in the corresponding frames (see Fig. 2) will not be taken into account for the georeferencing.

Once you are ready for the georeferencing, you can click on the button "Update Transform" (circle of arrows) in the toolbar of the reference frame (Fig. 2).  

## 4. Optimization of the interior and exterior orientations

If you would like the georeferencing to be taken into account for the calculation of interior and exterior orientations, you have to click on "Optimize Cameras" symbol (star icon in the toolbar of the reference frame). To perform camera optimization, it is best to select the "Adaptive Camera Model Fitting" and "Calculate covariance" options.  

The interior and exterior orientations can also be improved through the filtering of the tie points (i.e., the SPC), in order to remove the worst points that may influence the overall precision. This can be done with the tools provided in `Model > Gradual Selection...`. There are several filters available:

***Image count***  
If you have a good dataset with a lot of overlap between photos, it is best to start with "Image count". Select all tie points visible on two images and erase them using the "Delete Selection" button in the main upper toolbar. If this filter removes significant parts of your area of interest, you may consider not using this filtering option.

***Reprojection Error***  
High reprojection error usually indicates poor localization accuracy of the corresponding point projections at the point matching step. The values are normalised and without specific unit. It is also typical for false matches. Removing such points can improve accuracy of the subsequent optimization step. If your dataset is of good quality, you should be able to set a threshold below 1 without overfiltering the tie points.

***Reconstruction uncertainty***  
This is a complex metric that reflects how elongate the precision ellipse is on any point. More precisely, reconstruction uncertainty is ratio of the largest semi-axis to the smallest semi-axis of the error ellipse of the triangulated 3D point coordinates. The error ellipse corresponds to the uncertainty of the point triangulation alone without taking into account propagation of uncertainties from interior and exterior orientation parameters. Large values indicate elongated ellipses (for UAV surveys, this usually indicates luch weaker vertical precision than horizontal precision). Appropriate values to use as thresholds will vary between projects, and will depend on the number of images matched per point and the imaging geometry.  

***Projection accuracy***  
It corresponds to the average image scale that was used for measuring coordinates of the projections of the tie-point. This criterion allows to filter out points which projections were relatively poorely localized due to their "bigger size" (matching at different scales between images).  

It is suggested to use the filters in the order presented here.  

Once the filtering is performed properly, the interior and exterior orientations can be optimized using the star button in the reference frame (Fig. 2). Camera optimization can be performed only once, after both georeferencing and tie point filtering.  

Keep in mind that overfiltering can lead to worst results. To prevent that, avoid filtering that removes significant parts of the tie points within the area of interest. If you see a systematic pattern of point selection (e.g., circular selection of points in the corners of the image footprints), it is probably overfiltering. Try to prefer filtering that more or less select an homogeneous distribution of points.  

In any case, do not be afraid to remove the majority of tie points, as long as there is still a good distribution of points within your area of interest.  


## 5. Final Products

Once you are happy with the optimized interior and exterior orientations and the resulting georeferenced sparse point cloud, you are ready to produce the final 3D products. The first raw result will be a dense point cloud (DPC), from which a mesh or a digital elevation model (DEM) can be derived. Once a DEM is produced, it is possible to produce an orthophoto mosaic or "orthomosaic".

But before any processing, it is best to ensure that the bounding box surrounding the SPC (box delineated by gray lines) has the proper dimensions (dense matching will only apply for what is within this box) and is properly oriented with the coordinate system. To do that, you can use the python script provided in the repository, by loading it on `Tools > Run Scripts...`.  

#### 5.1 Dense matching  

To perform dense matching, go to `Workflow > Build Point Cloud...`. A small window will open. Select the following criteria:  
- Quality: Never use "Highest" and select either "High" or "Medium".  
- Depth Filtering: always select "Aggressive".  
- Other options: you can calculate the point colour and the point confidence. Untick these options if you don't need this information or if you would like to speed-up the processing.  

Dense matching is the most demanding processing step for the computer. Reducing the quality selection and reducing the size of the boudning box will reduce the computer needs for the calculation and, hence, the time needed to perform this step.

#### 5.2 DEM production  

To create a DEM, go to `Workflow > Build DEM...`. The spatial resolution cannot be modified and will be adapted depending on the point density of the DPC (will depend on the "quality" selected during dense matching). Select the proper coordinate system and the DPC as source data.

Interpolation is enabled by default. This option is useful for small holes within the DPC. If there are large holes in the DPC, the interpolation will lead to bad results. If this is the case, the best option is to keep the interpolation enabled and mask the large interpolation areas afterwards, e.g. within QGIS.


## Further references

In progress...

-------
***(c) B. Smets - Vrije Universiteit Brussel / Royal Museum for Central Africa, 2023***  
