Cyclops
=======

Exam grade recognition module. Still a prototype under active development. Please don't mind the mess.

# Requirements

- Python 2.7 (not compatible with Python 3)
- [OpenCV](http://opencv.org) 2.4+ with Python bindings
- [numpy](http://opencv.org)
- [zbar](http://zbar.sourceforge.net)

# Mac OS X Environment Setup

## Installing OpenCV with Python support

We recommend using the [Homebrew](http://brew.sh) package manager:

        brew tap homebrew/science
        brew install python
        brew install opencv
        brew install zbar

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
