# Image Downloader Tool
A small script I wrote for my manager to download/resize a whole bunch of images from a csv file.

# Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Troubleshooting](#troubleshooting)

## Installation
To install this script just clone this repo and copy the python file to a location on your `$PATH`:</br>
:exclamation: **You may also install the requirements**
```bash
git clone https://github.com/BaileyCPSG/imgdt.git
cd imgdt
pip install -r requirements.txt
cp src/imgdt.py path/to/destination
```

## Usage
To use this script use must have a csv file with the headers url and filename in that order. The filenames must contain the extension that you would like to use on the filename.

Program Execution looks like this:
1. Asks for the input csv file.
2. Asks for location of directory to store images in.
3. Downloads images to the image directory.
4. Asks user if they want to resize images.
5. If yes resizes images to a max of 600x600.

## Troubleshooting
If there are any errors during program execution they will be written to the log file. The log file is located in the src directory of the repo after first execution of script.
