#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest
import numpy as np
import numpy.testing as nt
import hypothesis as hy
from hypothesis.extra import numpy as hynp

from padvinder.ray import Ray

class TestRay(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the ray is constructed with the
        expected default parameters.
        """
        r = Ray()
        nt.assert_almost_equal(r.position, (0, 0, 0))
        nt.assert_almost_equal(r.direction, (1, 0, 0))
        nt.assert_almost_equal(r.position, r._position)
        nt.assert_almost_equal(r.direction, r._direction)

    def test_input(self):
        """
        Test if the input values are checked
        correctly.
        Values that do not validate the checks
        are omitted because they are covered by
        the remaining tests.
        """
        with self.assertRaises(ValueError):
            Ray(position=np.array((np.nan, 0, 0)))
        with self.assertRaises(ValueError):
            Ray(position=np.array((np.inf, 0, 0)))
        with self.assertRaises(ValueError):
            Ray(position=np.array((np.inf, 0, 0)))
        with self.assertRaises(ValueError):
            Ray(direction=np.array((np.nan, 0, 0)))
        with self.assertRaises(ValueError):
            Ray(direction=np.array((np.inf, 0, 0)))
        with self.assertRaises(ValueError):
            Ray(direction=np.array((-np.inf, 0, 0)))

    def test_point(self):
        """
        Test if a point with given distance along the
        ray is calculated correctly.
        """
        r = Ray((0, 0, 0), (1, 0, 0))
        nt.assert_almost_equal(r.point(0), r.position)
        nt.assert_almost_equal(r.point(1), r.position + r.direction)
        nt.assert_almost_equal(r.point(2), (2, 0, 0))

    def test_string(self):
        """
        Test if the string representation of the ray is correct. Because testing
        against a concrete string is tough if numpy changes how they print
        arrays - we will just test if the call succedes.
        """
        str(Ray())

    @hy.given(hynp.arrays(np.float64, (2, 3),
              hy.strategies.floats(min_value=-1e9, # beyond that all test errors
                                   max_value=1e9,  # are rounding errors
                                   allow_nan=False,
                                   allow_infinity=False)))
    def test_hypothesis(self, arg):
        """
        Test the ray's invariants with 'random' input from hypothesis
        """
        p, d = arg
        norm_d = np.linalg.norm(d)
        hy.assume(norm_d > 1e-8)
        r = Ray(p, d)
        nt.assert_almost_equal(r.position, p)
        nt.assert_almost_equal(r.direction*norm_d, d)
        nt.assert_almost_equal(np.linalg.norm(r.direction), 1)
        point = r.point(4)
        nt.assert_almost_equal(np.linalg.norm(r.position - point), 4)
