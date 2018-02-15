import numpy as np

import unittest
import numpy.testing as nt

from padvinder.ray      import Ray
from padvinder.geometry import Sphere
from padvinder.geometry import Plane
from padvinder.scene    import Scene

class TestScene(unittest.TestCase):
    def setUp(self):
        self.r1 = Ray()
        self.s1 = Sphere(position=(-2, 0, 0)) # intersect at np.inf
        self.s2 = Sphere(position=( 2, 0, 0)) # intersect at 1
        self.p1 = Plane(position=(3, 0, 0))   # intersect at np.inf
        self.p2 = Plane(position=(.5, 0, 0), normal=(1, 0, 0)) # at 0.5

        self.scn = Scene(self.s1, self.s2, self.p1, self.p2)

    def test_interator(self):
        for i, obj in enumerate(self.scn):
            self.assertTrue(self.scn._renderable[i] is obj)

        scn_iter = iter(self.scn)
        self.assertTrue(next(scn_iter) is self.s1)
        self.assertTrue(next(scn_iter) is self.s2)
        self.assertTrue(next(scn_iter) is self.p1)
        self.assertTrue(next(scn_iter) is self.p2)

    def test_intersection(self):
        (d, o) = self.scn.intersect(self.r1)
        nt.assert_almost_equal(d, 0.5)
        self.assertTrue(o is self.p2)

        r2 = Ray(direction=(0, 1, 0)) # does not intersect scene
        (d, o) = self.scn.intersect(r2)
        nt.assert_almost_equal(d, np.inf)
        self.assertIsNone(o)
