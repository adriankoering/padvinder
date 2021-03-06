#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
    Main routine that executes all tests.
"""
import unittest

from padvinder.test.test_util     import TestNormalize
from padvinder.test.test_util     import TestCheckFinite
from padvinder.test.test_ray      import TestRay
from padvinder.test.test_material import TestMaterial
from padvinder.test.test_material import TestEmission
from padvinder.test.test_material import TestLambert
from padvinder.test.test_geometry import TestGeometry
from padvinder.test.test_geometry import TestSphere
from padvinder.test.test_geometry import TestPlane
from padvinder.test.test_scene    import TestScene
from padvinder.test.test_camera   import TestCamera
from padvinder.test.test_camera   import TestPerspectiveCamera

unittest.main()
