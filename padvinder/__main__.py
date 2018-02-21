#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
The main entry point, tying everything together and producing a rendered image.

.. moduleauthor:: Adrian Köring
"""
from padvinder.material import Emission
from padvinder.material import Lambert

from padvinder.geometry import Plane
from padvinder.geometry import Sphere

from padvinder.scene    import Scene

def main():
    """
    This example sets up a scene and kicks off a render which is shown upon
    completion.
    """
    light = Emission()
    green = Lambert((0.2, 1.0, 0.2))
    red   = Lambert((1.0, 0.2, 0.2))
    p1 = Plane(light, (0, 10, 0))
    p2 = Plane(green, (0, -5, 0))

    s  = Sphere((0, 0, -5))

    scn = Scene(p1, p2, s)





if __name__ == "__main__":
    main()
