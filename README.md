![License:MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)
[![Build Status](https://travis-ci.org/adriankoering/padvinder.svg?branch=master)](https://travis-ci.org/adriankoering/padvinder)
[![Documentation Status](https://readthedocs.org/projects/padvinder/badge/?version=latest)](http://padvinder.readthedocs.io/en/latest/?badge=latest)


# Padvinder

Padvinder is a little pathtracing renderer written in Python. Originally I was keen to implement my own pathtracer. The focus has always been on quick coding and learning rather than on code performance. Over the time it developed into an exercise for good coding practices like test-driven-development, continuous integration and documentation.

Padvinder is meant to be a dutchly flavoured word for pathtracing; encoding the algorithm used for rendering with Guido van Rossum's dutch origins.

## Example Usage

Run an example renering from the root of the repository via
```
python -m padvinder
```
I find this to be cleaner and shorter than having a main.py file. It makes use of Python's ability to execute modules. Under the hood \_\_main\_\_.py is executed.

## Tests

Run the tests similarly to running the example via
```
python -m padvinder.test
```
Again, this executes the \_\_main\_\_.py file in the test module while keeping the command line concise.

## Continuous Integration

Thanks to [Travis CI](https://travis-ci.org/) :smiley: Find the build status at [Padvinder on Travis](https://travis-ci.org/adriankoering/padvinder).


## Documentation
Thanks to [Read the Docs](https://readthedocs.org/) :smiley: Find the documentation at [Padvinder on Read the Docs](http://padvinder.readthedocs.io/en/latest/).



Park old read the docs


# Padvinder

Padvinder is a little pathtracing renderer written in Python. Originally I was keen to implement my own pathtracer.

## Example Usage

Run an example renering from the root of the repository via
```
python -m padvinder
```
I find this to be cleaner and shorter than having a main.py file. It makes use of Python's ability to execute modules. Under the hood \_\_main\_\_.py is executed.

## Tests

Run the tests similarly to running the example via
```
python -m padvinder.test
```
Again, this executes the \_\_main\_\_.py file in the test module while keeping the command line concise.


# Ray

A ray has a starting _position_ and a _direction_ it is heading in. Both are three dimensional vectors and for simplicity the _direction_ is normalized to have a length of one.
