# Photogrammetric processing with Metashape Pro - A user guide

*(c) Benoît SMETS — Vrije Universiteit Brussel / Royal Museum for Central Africa*  
*Version 1.0 — 28 March 2023*   
#SfM-MVS #photogrammetry #Agisoft #Metashape #userguide

---------

<div style="text-align: justify">This user guide aims at summarising the procedure to perform a proper photogrammetric processing of photographs acquired with a digital camera, using the <a href="https://www.agisoft.com/">Agisoft Metashape Pro software</a>, for topographic reconstruction and/or orthorectified ground surface imaging. A similar workflow is applicable for the 3D modelling of objects, but specificities of such kind of photogrammetric processing are note covered here. If your purpose is to process scanned aerial photographs (with fiducial marks) or satellite images for 3D photogrammetric reconstruction, the explanations proposed in this guide are not appropriate. Other user guides will soon be proposed for these purposes.</div>

<div style="text-align: justify">In the present guide, it is assumed that the user already knows the fundamentals of Structure-from-Motion Multi-View Stereo (SfM-MVS) photogrammetry. Explanations will only focus on how to use Agisoft Metashape Pro to preform this type of processing.</div>

<div style="text-align: justify">As a final introductory word, I strongly suggest you to, first, read the <a href="https://www.agisoft.com/downloads/user-manuals/">user manual provided by Agisoft</a>, or at least to have it with you while going through this guide.</div>
<br>

## Preliminary conditions

<div style="text-align: justify">Nowadays, digital image acquisition is the most important step in SfM-MVS photogrammetry. Photogrammetry is a well established measurement method, with base equations developed during the 19th and 20th centuries. All available modern software programs can provide results of similar quality, as long as the imaging survey was performed in appropriate conditions, with the required equipment.</div>

<div style="text-align: justify">Hence, it is considered here that the image acquisition has been performed properly, with these key considerations taken into account:</div>

- *Good camera and lens (preferably fixed lens), with similar focal length between photo shots.*
- *Sharp and properly exposed photos.*
- *Important overlap (i.e., 70 to 90 %) between the photos, along- and across-track.*
- *Point of views sub-perpendicular to the main planes of the targeted surface.*
- *Convergent views, at least as a complement to the main image dataset.*
- If needed and/or possible, ground control points (GCPs) or coded targets homogenously distributed in the area of interest.
<br>

## Main Graphical User Interface (GUI)


Figure 1 shows the main GUI of Metashape pro, with the location of the main menus, toolbars and tabs. This figure help to understand the procedures described in this user guide.



<div style="text-align: center"><span style="color:SteelBlue">Figure 1 — Main Graphical User Interface (GUI) of Metashape Pro</span></div>


## 1. Image preparation


#### 1.1. Image pre-processing

<div style="text-align: justify">Image pre-processing may be required for your dataset, before doing any kind of photogrammetric processing. This especially the case when the photos were shot in RAW format. In any case, the image pre-processing must provide an optimal result for image matching, while avoiding contrast and tone differences between photographs, which would lead to colour variations in the final orthomosaic. The key aspects to take into account during this pre-processing:</div>

- Avoid under- and over-exposure
- Correct any vignetting or chromatic abberration visible in the imagery
- If illumination varied significantly during the photo acquisition, homogenise the contrast and tone using, e.g., histogram matching
- Avoid image compression as much as possible
- If useful, increase image sharpness through a sharpening processing

#### 1.2. Image import

<div style="text-align: justify">To import images in Metashape Pro, open the software, go to `Workflow > Add Photos...` and select the photos you would like to use. The photos will appear in a "Chunk" of the Workspace, which corresponds to a processing job in which you will have all the results of your processing. Once imported, the folder "Cameras" in the chunk will display the list of the photos and will specify between brackets that none of the photos are aligned.</div>

<div style="text-align: justify">The first reflex to have is to check that the software properly recognises the type of images you have imported. To do so, go to `Tools > Camera Calibration...` and look are the following parameters derived from the image metadata:</div>
- The camera group (left column) recognizes the camera model
- The camera type is set to "Frame" (corresponds to most of the cameras you will use)
- The pixel size is specified
- The focal length is correct

#### 1.3. Image quality

<div style="text-align: justify">Once you are sure that the photos are properly recognised by the software, the first processing step is to check the quality (i.e., sharpness and texture) of the photos. For this, Metashape Pro has an excellent tool that allows you to assess the image quality and eventually remove less good images.</div>

<div style="text-align: justify">Right-click on an image of the dataset, either in the chunk of in the "Photos" frame, and select `Estimate Image Quality...`. A small window entitled "Analyze Photos" will appear. In the "Apply to" section, select "All cameras" and click "OK". In the "Photos" frame, the column entitled "Quality" will now be filled with decimal values ranging between 0 (useless photo) and 1 (photo of perfect quality).</div>

<div style="text-align: justify">It is good practice to remove photos having a quality value lower than 0.7. You can even be more severe if images have an overall better quality. Use a lower quality value threshold only if removing photos with a quality lower than 0.7 significantly affect image overlap and, hence, the 3D reconstruction.</div>
<br>

## 2. Photo alignment


<div style="text-align: justify">You are now ready to start the photogrammetric processing. The first step is to detect remarkable points, called <b>"key points"</b> in the images, and find similar key points, called <b>"tie points"</b>, in image pairs. This two-step processing (i.e., key point detection and image matching) is called <b>"photo alignment"</b> in Metashape Pro. In this processing step, the interior and exterior orientations of the photos will be calculated thanks to the tie points.</div>

<div style="text-align: justify">First, go to `Workflow > Align Photos...`. A small window will open. In the "General" section set the accuracy to "Highest". Reduce to "High" or "Medium" if your dataset is of poor quality or if you cannot properly align all the images.</div>

<div style="text-align: justify">In the "Advanced" section, adapt the <u>key point limit per megapixel</u> if necessary. A value between <b>50,000</b> and <b>100,000</b> is usually enough, but higher values sometimes improve the results. To choose this value, you can run several time the photo alignment and check if you always reach this maximum key point value per photo or not. If this is the case, you may increase the value. For the <u>tie point limit</u>, the most convenient choice is to set it to <b>0</b>, which means that there is no limit. Such a setting will of course lead to a longer processing time, but usually provide the best results. The options "Exclude stationary tie points", "Guided image matching" and "Adaptive camera model fitting" can be selected.</div>

<div style="text-align: justify">Once the processing is finished, you will end up with a <u>Sparse Point Cloud (SPC)</u>, which correspond to the reprojection of the tie points in an arbitrary 3D space. If the images are geotagged, the software will automatically set the coordinate system into a geographic one (usually, lat/long coordinates, with the WGS84 datum). Point colour is derived from the photos and already allow to see the ground surface and objects (vegetation, buildings, etc.) in 3 dimensions. In the `Model > Show/Hide Items` menu, we can display or hide the position of the camera, the bounding box surrounding the 3D reconstruction (called "Region"), the trackball, the ground control points (called "markers"), etc.</div>

<div style="text-align: justify">To see the quality of the SPC, it is possible to calculate a variance and, then, see which points are best reprojected in 3D. To do so, go to the reference tab (see lower left tab selection) and click on the star symbol "Optimize Cameras" and, in the newly opened window, select the two options: "Adaptive camera model fitting" and "Estimate tie point covariance". In the toolbar menu, on the top of the main window, click on the small arrow next to the "Point cloud" icon and choose <u>"Point Cloud Variance"</u> to replace the colour of the points by a colour scale indicating the calculated variance. Points are now vectors with a lenght proportional to the variance. As long as points appear as points, and not lines, the variance is sufficiently good. Long and red vectors should be removed to improve the calculation of interior and exterior orientations. This filtering will be performed in Section 4.</div>
<br>

## 3. Georeferencing


The georeferencing of the 3D reconstruction can be performed in two ways: (1) using geotagged photos, and (2) using ground control points (GCPs).

The first approach is straightforward and performed automatically by the software, if it is able to properly read the image metadata. This georeferencing methods is accurate when the two following conditions are met:
- The image positions are homogenously distributed in space, both horizontally and vertically. Having image acquisitions solely in a same plane will significantly decrease the georeferencing precision in one dimension.
- The camera position is accurate thanks to a positionning performed with a differential GNSS method, either in real-time (i.e., Real-Time Kinematic or "RTK") or in post-processing (i.e., Post-Processing Kinematic or "PPK").

The second approach requires the measurement of GCPs on the field, using a proper geodetic equipment (i.e., differential GNSS or EDM).




## 4. Optimization of the interior and exterior orientations




## 5. Final Products





## Further references



-------
***(c) B. Smets - Vrije Universiteit Brussel / Royal Museum for Central Africa, 2023***  
