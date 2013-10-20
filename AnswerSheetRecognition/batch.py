#
# Reads all of INPUT_DIR/*
# Clean, and write the number of answers found in OUTPUT_DIR/*
# (including guide boxes)
#

import os, errno
import glob
from datetime import datetime

import cv2
import numpy as np

from HorizontalGuideLine import *

INPUT_DIR = "input"
OUTPUT_DIR = "output"

############################
# COMPUTER VISION METHODS  #
############################
def dilate(dilation_size, img):
    dilation_size = 2 * dilation_size + 1
    kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation_size, dilation_size))
    return cv2.dilate(img, kernel)

def erode(erosion_size, img):
    erosion_size = 2 * erosion_size + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erosion_size, erosion_size))
    return cv2.erode(img, kernel)

#############################
# GRADELY SPECIFIC METHODS  #
#############################
  
# Attributes are found empirically for best overral recognition score 
def clean(img):
    img = cv2.medianBlur(img, 11)
              
    img = erode(3, img)
    ret,img = cv2.threshold(img, 111, 150, cv2.THRESH_BINARY)

    img = dilate(4, img)
    img = erode(3, img)
    return img

# Find circles in given image. 
# Circles are: guide boxes (horizontal + vertical) + student answers
# Returns: (image, circles): image with circles printed, and the circles found.
def find_circles(img):
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 10, np.array([]), 5, 9, 4, 25)
    #if circles is not None:
      #for c in circles[0]:
        #cv2.circle(img, (c[0],c[1]), c[2], (200),2)
    return img, circles[0]

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# Returns: mistakes count.
def process_file(input_file, output_file):
    # Image Cleanup
    img = cv2.imread(input_file, cv2.CV_LOAD_IMAGE_GRAYSCALE) 
    cleaned_img = clean(img)
    #cv2.imwrite(output_file, cleaned_img)
    
    # Recognition.
    circles, circles_found = find_circles(cleaned_img)

    guideline = HorizontalGuideLine(circles_found)
    guideline.recognize(circles)
    
    cv2.imwrite(output_file.replace("img", "img_circle"), circles)
    return abs(total_expected_circles_per_picture - len(circles_found))

#############################
#           MAIN ;)         #
#############################
init = datetime.now()
input_folders = glob.glob(INPUT_DIR + "/*")
circles_overall_mistakes = 0
for folder in input_folders:
    output_folder = folder.replace(INPUT_DIR, OUTPUT_DIR)
    total_expected_circles_per_picture = int(output_folder.split("_")[1])
    mkdir(output_folder)
    circles_folder_mistakes = 0
    input_files = glob.glob(folder + "/*")
    print output_folder
    for file in input_files:
        mistakes_file = process_file(file, file.replace(INPUT_DIR, OUTPUT_DIR).replace("jpg", "png"))
        circles_folder_mistakes += mistakes_file
        circles_overall_mistakes += mistakes_file

    print "\t\tMistakes: " + str(circles_folder_mistakes)

# QA: overall time & mistakes.
end = datetime.now()
#expected_overall_circles = len(input_files) * TOTAL_EXPECTED_CIRCLES_PER_PICTURE

print "\t\tMistakes total: " + str(circles_overall_mistakes)
print str((end - init)) + "s."