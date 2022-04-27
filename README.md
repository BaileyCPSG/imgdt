# Image Downloader Tool
A small script I wrote for my manager to download/resize a whole bunch of images from a csv file.

# Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Troubleshooting](#troubleshooting)

## Installation
To install this script just clone this repo, install the requirements, and run the main.py file:</br>
```bash
git clone https://github.com/BaileyCPSG/imgdt.git
cd imgdt
pip install -r requirements.txt
python src/main.py
```

## Usage
To use this script use must have a csv file with the headers url and filename in that order. The filenames must contain the extension that you would like to use on the filename.

Program Execution looks like this:
1. Enter the location of the input csv file.
2. Enter the location of directory to store downloaded images in.
3. Decide whether or not to resize.
4. Downloads images to the image directory.
5. If Resize was checked resizes images to a max of 600x600.

## Troubleshooting
If there are any errors during program execution they will be written to the log file. The log file is located in the src directory of the repo after first execution of script.<br>
Also the success file is in the same location with.
