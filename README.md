Cyclops
=======

Answer sheet optical recognition proof of concept using Python and OpenCV. I've written some custom Computer Vision and Linear Algebra algorithms.

Still a prototype under heavy development. Please don't mind the mess.

![Screenshot 01](Screenshots/01.png)

# Requirements

- Python 3.6+
- [OpenCV](http://opencv.org) 3.4+ with Python bindings
- [numpy](http://www.numpy.org)
- [zbar](http://zbar.sourceforge.net)

# Setup

These instructions cover macOS only, although it might be possible to setup the application in any Unix compatible environment.

## Installing OpenCV with Python support

We recommend using the [Homebrew](http://brew.sh) package manager:

        brew install opencv3

Follow the "Caveat" instructions from Homebrew in order to link OpenCV with Python.

To check if everything is working, open the python console and try to import the cv2 package. If you didn't get any errors it means everything is probably OK.

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
