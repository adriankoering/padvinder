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

unittest.main()
