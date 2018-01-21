Cyclops
=======

Answer sheet optical recognition proof of concept using Python and OpenCV. I've written some custom Computer Vision and Linear Algebra algorithms.

Still a prototype under heavy development. Please don't mind the mess.

![Screenshot 01](Screenshots/01.png)

# Requirements

- Python 3.6+
- [Pipenv](https://pypi.python.org/pypi/pipenv)
- [OpenCV](http://opencv.org) 3.4+ with Python bindings
- [zbar](http://zbar.sourceforge.net)

# Setup

These instructions cover macOS only, although it might be possible to setup the application in any Unix compatible environment.

For macOS, we recommend using the [Homebrew](http://brew.sh) package manager.

## Installing OpenCV with Python bindings

```sh
$ brew install opencv3
```

It may be necessary to follow the "Caveat" instructions from Homebrew in order to link OpenCV with Python.

To check if everything is working, open the Python 3 console and try to import the `cv2` package.

## Installing ZBar

```sh
$ brew install zbar
```

This will install the `zbarimg` command.

## Installing Pipenv

```sh
$ brew install pipenv
```

## Creating the virtual environment

Run the [`scripts/create-env.sh`](scripts/create-env.sh) script to bootstrap Pipenv and install dependencies.

# Running the Application

Run the [`cyclops.sh`](cyclops.sh) script passing as argument one of the images from the [`Samples`](Samples) folder.

There's a real-time interactive camera mode that can be activated using [`cyclops-camera.sh`](cyclops-camera.sh). You can print an answer sheet and show it to the camera on your computer. Works best if the paper is displayed horizontally.

# Running Automated Tests

Run the [`scripts/test.sh`](scripts/test.sh) script to run the suite of automated tests.

You can run a quick sanity integration test to check the health of the algorithms through the script [`scripts/sanity-check.sh`](scripts/sanity-check.sh).
