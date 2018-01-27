import unittest
import numpy as np
import numpy.testing as nt

from padvinder.ray import Ray

class TestRay(unittest.TestCase):
    def test_default_construction(self):
        """
        Test if the ray is constructed with The
        expected default parameters.
        """
        r = Ray()
        nt.assert_almost_equal(r.p, (0, 0, 0))
        nt.assert_almost_equal(r.d, (1, 0, 0))
        nt.assert_almost_equal(r.p, r._p)
        nt.assert_almost_equal(r.d, r._d)

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
        Ray(position=np.array((np.nan, 0, 0)), check_input=False)
        Ray(position=np.array((np.inf, 0, 0)), check_input=False)
        Ray(direction=np.array((np.nan, 0, 0)), check_input=False)
        Ray(direction=np.array((np.inf, 0, 0)), check_input=False)
