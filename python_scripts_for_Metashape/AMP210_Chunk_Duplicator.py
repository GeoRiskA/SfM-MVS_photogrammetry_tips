#-------------------------------------------------------------------------------
# Name:         AMP210_Chunk_Duplicator.py
# Purpose:      Duplicate a given chunk multiple times, based on the need of
#               the user.
#
# Compatibility: Agisoft Metashape Pro 2.1.x
#
# Version 210 (Compatible with AMP 2.1.0) – 11 April 2024
#
# Author:
#     Benoît Smets
#     Royal Museum for Central Africa / Vrije Unversiteit Brussel (Belgium)
#
# Important Note:   Before use, the name of the chunk to duplicate and the
#                   number of duplication must be first hard-coded in the
#                   script.
#-------------------------------------------------------------------------------

################################################################################
###############################    SETUP AREA    ###############################
################################################################################

# Name of the chunk to duplicate
chunk_name = "Your_chunk_name"

# Number of duplication to perform
number = 10

###############################   END OF SETUP   ###############################
################################################################################

print("CHUNK DUPLICATOR")
print("================")
print(" ")

import Metashape

doc = Metashape.app.document

for chunk in doc.chunks:
    if chunk.label == chunk_name:
        print(f"--> Chunk to duplicate = {chunk_name}")
        print(' ')
        for i in range(number):
            chunk.copy()
        print(' ')
        print(f"--> Chunk duplicated {number} times successfully")
