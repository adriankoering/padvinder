#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest
import numpy as np
import numpy.testing as nt
import hypothesis as hy
from hypothesis.extra import numpy as hynp

from padvinder.ray      import Ray
from padvinder.geometry import Geometry
from padvinder.geometry import Sphere
from padvinder.material import Material


class TestGeometry(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the geometry is constructed with the
        expected default parameters.
        """
        g = Geometry()
        nt.assert_almost_equal(g.material.color, Material().color)

    def test_non_default_construction(self):
        """
        Test if the geometry is constructed correctly
        with the non-default parameters.
        """
        g = Geometry(Material((1,1,1)))
        nt.assert_almost_equal(g.material.color, (1, 1, 1))

    def test_representation(self):
        """
        Test if the geometry class is capable of printing itself.
        """
        # as comparing to groundtruth gets more and more cumbersome
        # within this hierarchy, I will settle with confirming that
        # the function call succedes.
        try:
            s = str(Geometry())
        except:
            self.fail("TestGeometry.test_representation failed")

class TestSphere(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the sphere is constructed correctly
        with non-default parameters.
        """
        s = Sphere()
        nt.assert_almost_equal(s.material.color, Material().color)

    def test_non_default_construction(self):
        """
        Test if the sphere is constructed correctly
        with the expected default parameters.
        """
        s = Sphere(Material((1,1,1)))
        nt.assert_almost_equal(s.material.color, (1, 1, 1))

    def test_intersect(self):
        s = Sphere()
        nt.assert_almost_equal(s.intersect(Ray()), 1)
        r = Ray(position=(-10, 0, 0))
        nt.assert_almost_equal(s.intersect(r), 9)
        r = Ray(position=(0, -5, 0), direction=(0, 1, 0))
        nt.assert_almost_equal(s.intersect(r), 4)
        r = Ray(position=(10, 0, 0), direction=(1, 0, 0))
        nt.assert_almost_equal(s.intersect(r), np.inf)
        r = Ray(position=(0, 0, 10), direction=(0, 0, -1))
        nt.assert_almost_equal(s.intersect(r), 9)
        # r = Ray(position=(), direction=())
        # nt.assert_almost_equal(s.intersect(r), (1, 0, 0))
        # r = Ray(position=(), direction=())
        # nt.assert_almost_equal(s.intersect(r), (1, 0, 0))

    def test_normal(self):
        s = Sphere()
        nt.assert_almost_equal(s.normal((1, 0, 0)), (1, 0, 0))
        nt.assert_almost_equal(s.normal((0, 1, 0)), (0, 1, 0))
        nt.assert_almost_equal(s.normal((0, 0, 1)), (0, 0, 1))

    def test_representation(self):
        """
        Test if the sphere class is capable of printing itself.
        """
        # as comparing to groundtruth gets more and more cumbersome
        # within this hierarchy, I will settle with confirming that
        # the function call succedes.
        try:
            s = str(Sphere())
        except:
            self.fail("TestSphere.test_representation failed")

class TestPlane(Geometry):
    def test_default_construction(self):
        """
        Test if the plane is constructed correctly
        with non-default parameters.
        """
        p = Plane()
        nt.assert_almost_equal(p.material.color, Material().color)

    def test_non_default_construction(self):
        """
        Test if the plane is constructed correctly
        with the expected default parameters.
        """
        p = Plane(Material((1,1,1)))
        nt.assert_almost_equal(p.material.color, (1, 1, 1))

    def test_intersect(self):
        r = Ray()
        nt.assert_almost_equal(Plane().intersect(r), np.inf)

        p = Plane(position=(0.5, 0, 0), normal=(1, 0, 0))
        nt.assert_almost_equal(p.intersect(r), 0.5)

    def test_normal(self):
        p = Plane()
        nt.assert_almost_equal(s.normal((1, 0, 0)), (0, 1, 0))
        nt.assert_almost_equal(s.normal((0, 1, 0)), (0, 1, 0))
        nt.assert_almost_equal(s.normal((0, 0, 1)), (0, 1, 0))
        p = Plane(normal=(-1, 0, 0))
        nt.assert_almost_equal(s.normal((1, 0, 0)), (-1, 0, 0))
        nt.assert_almost_equal(s.normal((0, 1, 0)), (-1, 0, 0))
        nt.assert_almost_equal(s.normal((0, 0, 1)), (-1, 0, 0))

    def test_representation(self):
        """
        Test if the plane class is capable of printing itself.
        """
        # as comparing to groundtruth gets more and more cumbersome
        # within this hierarchy, I will settle with confirming that
        # the function call succedes.
        try:
            s = str(Plane())
        except:
            self.fail("TestSphere.test_representation failed")
