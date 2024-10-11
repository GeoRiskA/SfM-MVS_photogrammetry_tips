#!/bin/zsh

# Announce the processing in the terminal
echo " "
echo "============================================"
echo "  SORTING DJI MAVIC 3 MULTISPECTRAL IMAGES  "
echo "============================================"
echo " "
echo " >>> In progress..."

# Check if the correct number of arguments is passed
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_folder> <output_folder>"
  exit 1
fi

# Input and output folders
input_folder=$1
output_folder=$2

# Check if the input folder exists
if [ ! -d "$input_folder" ]; then
  echo "Error: Input folder does not exist."
  exit 1
fi

# Create the output folders if they don't exist
mkdir -p "$output_folder/G"
mkdir -p "$output_folder/R"
mkdir -p "$output_folder/RE"
mkdir -p "$output_folder/NIR"

# Move the images based on their suffix
for file in "$input_folder"/*.TIF; do
  if [[ $file == *_G.TIF ]]; then
    mv "$file" "$output_folder/G/"
  elif [[ $file == *_R.TIF ]]; then
    mv "$file" "$output_folder/R/"
  elif [[ $file == *_RE.TIF ]]; then
    mv "$file" "$output_folder/RE/"
  elif [[ $file == *_NIR.TIF ]]; then
    mv "$file" "$output_folder/NIR/"
  fi
done

# Announce its completion in the terminal
echo " "
echo "Images sorted and moved successfully!"
echo " "