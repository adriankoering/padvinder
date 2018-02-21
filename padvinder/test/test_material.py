#!/usr/bin/python
# -*- coding: latin-1 -*-

import unittest
import numpy as np
import numpy.testing as nt
import hypothesis as hy
from hypothesis.extra import numpy as hynp

from padvinder.util     import normalize
from padvinder.material import Material
from padvinder.material import Emission
from padvinder.material import Lambert

class TestMaterial(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the material is constructed with the
        expected default parameters.
        """
        m = Material()
        nt.assert_almost_equal(m.color, (0.5, 0.5, 0.5))
        nt.assert_almost_equal(m.color, m(None, None, None, None))

    def test_non_default_construction(self):
        """
        Test if the material is constructed correctly with
        non-default parameters.
        """
        m = Material((1,1,1))
        nt.assert_almost_equal(m.color, (1,1,1))
        nt.assert_almost_equal(m.color, m(None, None, None, None))

    @hy.given(hynp.arrays(np.float64, 3,
              hy.strategies.floats(min_value=-1e9, # beyond that test errors
                                   max_value=1e9,  # are rounding errors
                                   allow_nan=False,
                                   allow_infinity=False)))
    def test_outgoing_direction(self, normal):
        hy.assume(0.001 < np.linalg.norm(normal) < 1e18)
        normal = normalize(normal)
        m = Material()
        d = m.outgoing_direction(normal, None)
        self.assertTrue(np.dot(normal, d) > 0)


    def test_representation(self):
        """
        Test if the string representation of the material is correct.
        Because testing against a concrete string is tough if numpy changes how
        they print arrays, we will just test if the call succedes.
        """
        try:
            s = str(Material())
        except:
            self.fail("TestMaterial.test_representation failed")


class TestEmission(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the material is constructed with the
        expected default parameters.
        """
        m = Emission()
        nt.assert_almost_equal(m.color, (10, 10, 10))
        nt.assert_almost_equal(m.color, m(None, None, None, None))

    def test_non_default_construction(self):
        """
        Test if the material is constructed correctly with
        non-default parameters.
        """
        m = Emission((1,1,1))
        nt.assert_almost_equal(m.color, (1,1,1))
        nt.assert_almost_equal(m.color, m(None, None, None, None))

    def test_representation(self):
        """
        Test if the string representation of the emission is correct.
        Because testing against a concrete string is tough if numpy changes how
        they print arrays, we will just test if the call succedes.
        """
        try:
            s = str(Emission())
        except:
            self.fail("TestEmission.test_representation failed")


class TestLambert(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the material is constructed with the
        expected default parameters.
        """
        m = Lambert()
        nt.assert_almost_equal(m.color, (0.5, 0.5, 0.5))
        # nt.assert_almost_equal(m.color, m(None, None, None, None))

    def test_non_default_construction(self):
        """
        Test if the material is constructed correctly with
        non-default parameters.
        """
        m = Lambert((1,1,1))
        nt.assert_almost_equal(m.color, (1,1,1))
        # nt.assert_almost_equal(m.color, m(None, None, None, None))

    def test_representation(self):
        """
        Test if the string representation of the material is correct.
        Because testing against a concrete string is tough if numpy changes how
        they print arrays, we will just test if the call succedes.
        """
        try:
            s = str(Lambert())
        except:
            self.fail("TestLambert.test_representation failed")
