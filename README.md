Cyclops
=======

Answer sheet optical recognition proof of concept using Python and OpenCV. I've written some custom Computer Vision and Linear Algebra algorithms.

Still a prototype under heavy development. Please don't mind the mess.

![Screenshot 01](Screenshots/01.png)

# Requirements

- Python 2.7 (not compatible with Python 3)
- [OpenCV](http://opencv.org) 2.4+ with Python bindings
- [numpy](http://opencv.org)
- [zbar](http://zbar.sourceforge.net)

# Setup

Only OS X is supported at the moment.

## Installing OpenCV with Python support

We recommend using the [Homebrew](http://brew.sh) package manager:

        brew tap homebrew/science
        brew install opencv

You need to link the OpenCV libraries installed by Homebrew into the Python library directory. At the time of this writing, the current OpenCV version is 2.4.10.1. 

        cd /Library/Python/2.7/site-packages/
        sudo ln -s /usr/local/Cellar/opencv/2.4.10.1/lib/python2.7/site-packages/cv.py cv.py
        sudo ln -s /usr/local/Cellar/opencv/2.4.10.1/lib/python2.7/site-packages/cv2.so cv2.so

Update your PYTHONPATH environment variable:

        echo "export PYTHONPATH=/usr/local/lib/python2.7/site-packages/:$PYTHONPATH" >> ~/.bash_profile

Close and reopen the Terminal. Open the python console and try to import the cv2 package:

        python import cv2

If you didn't get any errors after importing the cv2 package it means everything is OK.

## Installing ZBar

Zbar can be installed using Homebrew:

        brew install zbar

This will install the **zbarimg** command.

# Running The Prototype

Run the `cyclops.sh` script passing as argument one of the images from the `Samples` folder.

There's a real-time interactive camera mode that can be activated using `cyclops-camera.sh`. You can print an answer sheet and show it to the camera on your computer. Works best if the paper is displayed horizontally.

# Running Automated Tests

Run the `unit-test.sh` script to run the suite of automated unit tests.

You can run a quick sanity integration test to check the health of the algorithms through the script `sanity-test.sh`.
