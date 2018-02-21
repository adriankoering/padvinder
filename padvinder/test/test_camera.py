#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest
import numpy as np
import numpy.testing as nt

from padvinder.util   import normalize
from padvinder.camera import Camera
from padvinder.camera import PerspectiveCamera

class TestCamera(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the camera is constructed with the
        expected default parameters.
        """
        c = Camera()
        nt.assert_almost_equal(c.position, (0, 0, 0))
        nt.assert_almost_equal(c.up, (0, 1, 0))
        nt.assert_almost_equal(c.optical_axis, (0, 0, 1))

    def test_custom_construction(self):
        """
        Test if the camera is constructed correctly
        with the non-default parameters.
        """
        c = Camera((10, 5, 0), (0, -1, 0), (10, 5, 1))
        nt.assert_almost_equal(c.position, (10, 5, 0))
        nt.assert_almost_equal(c.up, (0, -1, 0))
        nt.assert_almost_equal(c.optical_axis, (0, 0, 1))

    def test_invalid_construction(self):
        """
        Test if the camera construction fails as expected on invalid input
        """
        with self.assertRaises(ValueError):
            Camera(position=(0, 0, 0), look_at=(0, 0, 0))
        with self.assertRaises(ValueError):
            Camera(up=(-np.inf, 0, np.nan))
        with self.assertRaises(ZeroDivisionError):
            Camera(up=(0, 0, 0))

    def test_representation(self):
        """
        Test if the camera class is capable of printing itself.
        """
        # as comparing to groundtruth gets more and more cumbersome
        # within this hierarchy, I will settle with confirming that
        # the function call succedes.
        try:
            s = str(Camera())
        except:
            self.fail("TestCamera.test_representation failed")

class TestPerspectiveCamera(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the perspective camera is constructed
        with the expected default parameters.
        """
        c = PerspectiveCamera()
        nt.assert_almost_equal(c.position, (0, 0, 0))
        nt.assert_almost_equal(c.up, (0, 1, 0))
        nt.assert_almost_equal(c.optical_axis, (0, 0, 1))
        nt.assert_almost_equal(c.focal_length, 24)
        nt.assert_almost_equal(c._image_plane_center, (0, 0, 1))

    def test_custom_construction(self):
        """
        Test if the perspective camera is constructed
        correctly with the non-default parameters.
        """
        c = PerspectiveCamera((10, 5, 0), (0, -1, 0), (10, 5, 1), 48)
        nt.assert_almost_equal(c.position, (10, 5, 0))
        nt.assert_almost_equal(c.up, (0, -1, 0))
        nt.assert_almost_equal(c.optical_axis, (0, 0, 1))
        nt.assert_almost_equal(c.focal_length, 48)
        nt.assert_almost_equal(c._image_plane_center, (10, 5, 2))

    def test_invalid_construction(self):
        """
        Test if the camera construction fails as expected on invalid input
        """
        with self.assertRaises(ValueError):
            PerspectiveCamera(position=(0, 0, 0), look_at=(0, 0, 0))
        with self.assertRaises(ValueError):
            PerspectiveCamera(up=(-np.inf, 0, np.nan))
        with self.assertRaises(ZeroDivisionError):
            PerspectiveCamera(up=(0, 0, 0))
        with self.assertRaises(ValueError):
            PerspectiveCamera(focal_length=-2)

    def test_ray(self):
        """
        Test if the initial rays are calculated correctly - Beware that the
        indexing is following numpy's convention: x is vertical & y is
        horizontal.
        """
        c = PerspectiveCamera()
        r = c.ray((50, 50), (100, 100), False)
        nt.assert_almost_equal(r.position, (0, 0, 0))
        nt.assert_almost_equal(r.direction, (0, 0, 1))

        r = c.ray((0, 0), (100, 100), False)
        nt.assert_almost_equal(r.direction, normalize((1, 1, 1)))

        r = c.ray((100, 0), (100, 100), False)
        nt.assert_almost_equal(r.direction, normalize((1, -1, 1)))

        r = c.ray((0, 100), (100, 100), False)
        nt.assert_almost_equal(r.direction, normalize((-1, 1, 1)))

        r = c.ray((100, 100), (100, 100), False)
        nt.assert_almost_equal(r.direction, normalize((-1, -1, 1)))

    def test_representation(self):
        """
        Test if the perspective camera class is capable of printing itself.
        """
        # as comparing to groundtruth gets more and more cumbersome
        # within this hierarchy, I will settle with confirming that
        # the function call succedes.
        try:
            s = str(PerspectiveCamera())
        except:
            self.fail("TestPerspectiveCamera.test_representation failed")
