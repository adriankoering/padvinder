import unittest
import numpy as np
import numpy.testing as nt
import hypothesis as hy
from hypothesis.extra import numpy as hynp

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

    def test_representation(self):
        """
        Test if the material can print itself correctly
        """
        self.assertEqual(str(Material()),
                         "Material(color=[0.5 0.5 0.5])")


class TestEmission(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the material is constructed with the
        expected default parameters.
        """
        m = Emission()
        nt.assert_almost_equal(m.color, (0.5, 0.5, 0.5))
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
        Test if the material can print itself correctly
        """
        self.assertEqual(str(Emission()),
                         "Emission(color=[0.5 0.5 0.5])")


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
        Test if the material can print itself correctly
        """
        self.assertEqual(str(Lambert()),
                         "Lambert(color=[0.5 0.5 0.5], diffuse=1)")
