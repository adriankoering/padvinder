import unittest
import numpy as np
import numpy.testing as nt
import hypothesis as hy
from hypothesis.extra import numpy as hynp

from padvinder.util import normalize

class TestNormalize(unittest.TestCase):
    def test_invalid_examples(self):
        """
        Test if normalize rejects invalid parameters as expected.
        """
        with self.assertRaises(ValueError):
            normalize((np.inf, 0, 0))
        with self.assertRaises(ValueError):
            normalize((np.nan, 0, 0))
        with self.assertRaises(ValueError):
            normalize((-np.inf, 0, 0))
        with self.assertRaises(ZeroDivisionError):
            normalize((0, 0, 0))

    @hy.given(hynp.arrays(np.float64, 3,
              hy.strategies.floats(min_value=-1e9, # beyond that test errors
                                   max_value=1e9,  # are rounding errors
                                   allow_nan=False,
                                   allow_infinity=False)))
    def test_hypothesis(self, v):
        """
        Test normalize's invariants with 'random' input from hypothesis.
        """
        norm_v = np.linalg.norm(v)
        hy.assume(norm_v > 1e-8)
        nt.assert_almost_equal(np.linalg.norm(normalize(v)), 1)
        nt.assert_almost_equal(normalize(v)*norm_v, v)
