Cyclops - Python
================

Exam grade recognition module - Python implementation

# Requirements
- Python 2.7+ (not compatible with Python 3)
- [OpenCV](http://opencv.org) 2 with Python bindings
- [numpy](http://opencv.org)
- [zbar](http://zbar.sourceforge.net)

# Mac OS X Environment Setup

We recommend using the [Homebrew](http://brew.sh) package manager.

## Installing OpenCV with Python Support

-   Install XCode command tools: Open XCode -> Preferences -> Downloads -> Components -> Command Line Tools

-   Install CMake. On Homebrew: brew install cmake

-   Install [ScipySuperpack](https://github.com/fonnesbeck/ScipySuperpack): 

        curl https://raw.github.com/fonnesbeck/ScipySuperpack/master/install_superpack.sh > install_superpack.sh
        sh install_superpack.sh

-   Download and extract OpenCV 2.4+. Change to the extracted opencv directory and type:

        mkdir release cd release cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D BUILD_EXAMPLES=ON ..
        make -j8
        sudo make install

-   Update your PYTHONPATH environment variable:

        echo "export PYTHONPATH=/usr/local/lib/python2.7/site-packages/:$PYTHONPATH" >> ~/.bash_profile

-   Close and reopen the Terminal. Open the python console and try to import the cv2 package:

        python import cv2

    If you didn't get any errors after importing the cv2 package it means everything is OK.

## Installing numpy

    [sudo] pip install numpy

## Installing ZBar

Zbar can be installed using Homebrew:

    brew install zbar

This will install the **zbarimg** command.