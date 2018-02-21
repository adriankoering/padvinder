#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
The main entry point, tying everything together and producing a rendered image.

.. moduleauthor:: Adrian Köring
"""

from padvinder.ray import Ray

def main():
    """
    This example sets up a scene and kicks off a render which is shown upon
    completion.
    """
    print("Hello Padvinder")
    print("Default Ray - {}".format(Ray()))


if __name__ == "__main__":
    main()
