import unittest
import numpy.testing as nt

from padvinder.ray import Ray

class TestRay(unittest.TestCase):
    def test_default_construction(self):
        r = Ray()
        nt.assert_almost_equal(r.p, (0, 0, 0))
        nt.assert_almost_equal(r.d, (1, 0, 0))
        nt.assert_almost_equal(r.p, r._p)
        nt.assert_almost_equal(r.d, r._d)
