#-------------------------------------------------------------------------------
# Name:         AMP210_Chunk_Duplicator_4band_MS.py
# Purpose:      Duplicate a given chunk 4 times, i.e., one per spectral band.
#
# Compatibility: Agisoft Metashape Pro 2.1.x
#
# Version 210 (Compatible with AMP 2.1.0) – 28 October 2024
#
# Author:
#     Benoît Smets
#     Royal Museum for Central Africa / Vrije Unversiteit Brussel (Belgium)
#
# Important Note:   When running the script, the name of the chunk to duplicate
#                   must be entered as an argument in Metashape Pro.
#-------------------------------------------------------------------------------

print(" ")
print("====================================================")
print("   CHUNK DUPLICATOR FOR 4-BAND MULTISPECTRAL DATA   ")
print("====================================================")
print(" ")

import Metashape
import sys

# Chunk name to enter as argument when running the script in Metashape
chunk_name = sys.argv[1]

doc = Metashape.app.document

for chunk in doc.chunks:
    if chunk.label == chunk_name:
        print(f"--> Chunk to duplicate = {chunk_name}")
        print(' ')
        duplicate1 = chunk.copy()
        duplicate1.label = chunk_name + "_GREEN"
        duplicate2 = chunk.copy()
        duplicate2.label = chunk_name + "_RED"
        duplicate3 = chunk.copy()
        duplicate3.label = chunk_name + "_REDEDGE"
        duplicate4 = chunk.copy()
        duplicate4.label = chunk_name + "_NIR"
        print(' ')
        print(f"--> Chunk duplicated 4 times successfully")

print(" ")
print("======================================================")
print("   END OF CHUNK DUPLICATOR FOR 4-BAND MULTISPECTRAL   ")
print("======================================================")
print(" ")
