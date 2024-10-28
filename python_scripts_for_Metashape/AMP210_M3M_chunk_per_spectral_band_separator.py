#-------------------------------------------------------------------------------
# Name:         AMP210_M3M_chunk_per_spectral_band_separator.py
# Purpose:      Duplicate a given chunk 4 times, i.e., one per spectral band
#               and remove undesired cameras in each duplicated chunk.
#
# Compatibility: Agisoft Metashape Pro 2.1.x
#
# Version 210 (Compatible with AMP 2.1.0) – 28 October 2024
#
# Author:
#     Benoît Smets
#     Royal Museum for Central Africa / Vrije Unversiteit Brussel (Belgium)
#
# Important Note:   Two conditions must be met to run the script:
#                   1) The name of the chunk to duplicate must be entered as
#                      an argument when running the script in Metashape.
#                   2) The photos of each spectral band must be grouped by
#                      sensor type, with the exact following names for each
#                      sensor group: 'GREEN', 'RED', 'REDEDGE', 'NIR'.
#-------------------------------------------------------------------------------

print(" ")
print("====================================================")
print("   CHUNK DUPLICATOR FOR 4-BAND MULTISPECTRAL DATA   ")
print("====================================================")
print(" ")

import Metashape
import sys

# ARGUMENT: Chunk name to enter as argument when running the script in Metashape
chunk_name = sys.argv[1]

# 1) Duplicate the chunk 4 times (one per spectral band)

print(' ')
print("STEP 1: Chunk duplication in progress...")
print("----------------------------------------")

doc = Metashape.app.document

for chunk in doc.chunks:
    # Duplicate the chunk 4 times and rename them
    if chunk.label == chunk_name:
        duplicate1 = chunk.copy()
        duplicate1.label = chunk_name + "_GREEN"
        duplicate2 = chunk.copy()
        duplicate2.label = chunk_name + "_RED"
        duplicate3 = chunk.copy()
        duplicate3.label = chunk_name + "_REDEDGE"
        duplicate4 = chunk.copy()
        duplicate4.label = chunk_name + "_NIR"

print(' ')
print("--> Chunk duplicated 4 times successfully")

# 2) Remove undesired camera groups in each duplicated chunk

print(' ')
print("STEP 2: Remove of undesired cameras per chunk in progress...")
print("------------------------------------------------------------")

# Green band
for dup_chunk in doc.chunks:
    if dup_chunk.label == chunk_name + "_GREEN":
        for camera in dup_chunk.cameras:
            if camera.sensor.label == 'RED':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'REDEDGE':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'NIR':
                dup_chunk.remove(camera)

# Red band
for dup_chunk in doc.chunks:
    if dup_chunk.label == chunk_name + "_RED":
        for camera in dup_chunk.cameras:
            if camera.sensor.label == 'GREEN':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'REDEDGE':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'NIR':
                dup_chunk.remove(camera)

# RedEdge band
for dup_chunk in doc.chunks:
    if dup_chunk.label == chunk_name + "_REDEDGE":
        for camera in dup_chunk.cameras:
            if camera.sensor.label == 'GREEN':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'RED':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'NIR':
                dup_chunk.remove(camera)

# NIR band
for dup_chunk in doc.chunks:
    if dup_chunk.label == chunk_name + "_NIR":
        for camera in dup_chunk.cameras:
            if camera.sensor.label == 'GREEN':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'RED':
                dup_chunk.remove(camera)
            elif camera.sensor.label == 'REDEDGE':
                dup_chunk.remove(camera)

print(' ')
print("--> Unnecessary cameras successfully removed from each chunk")

print(" ")
print("   END OF CHUNK DUPLICATOR FOR 4-BAND MULTISPECTRAL   ")
print("======================================================")
print(" ")