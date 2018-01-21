# Cyclops

Answer sheet optical recognition proof of concept using Python and OpenCV.
I've written some custom Computer Vision and Linear Algebra algorithms.

![Screenshot 01](Screenshots/01.png)

## Requirements

- Python 3.6+
- [Pipenv](https://pypi.python.org/pypi/pipenv)
- [OpenCV](http://opencv.org) 3.4+ with Python bindings
- [zbar](http://zbar.sourceforge.net)

## Setup

These instructions cover macOS only, although it might be possible to setup the
application in any Unix compatible environment.

For macOS, we recommend using the [Homebrew](http://brew.sh) package manager.

### Installing OpenCV with Python bindings

```sh
$ brew install opencv3
```

It may be necessary to follow the "Caveat" instructions from Homebrew in order
to link OpenCV with Python.

To check if everything is working, open the Python 3 console and try to import
the `cv2` package.

### Installing ZBar

```sh
$ brew install zbar
```

This will install the `zbarimg` command.

### Installing Pipenv

```sh
$ brew install pipenv
```

### Creating the virtual environment with dependencies

```sh
$ scripts/create-env.sh
```

## Running the application

Run the `cyclops.sh` script passing as argument one of the images
from the [`Samples`](Samples) folder.

There's a real-time interactive camera mode that can be activated using the
`cyclops-camera.sh` script. You can print an answer sheet and show it to the
camera on your computer. Works best if the paper is displayed horizontally.

## Automated checks

### Unit tests

```sh
$ scripts/test.sh
```

### Sanity check

You can run a quick sanity integration test to check the health of the
algorithms through the script:

```sh
$ scripts/sanity-check.sh
```

### Code style

```sh
$ scripts/style-check.sh
```

This project must adhere to the
[PEP-8](https://www.python.org/dev/peps/pep-0008/) style guide.
