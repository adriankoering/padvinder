"""
Rays are stand-ins for lightrays heading from the camera through the scene.

.. moduleauthor:: Adrian Köring
"""

import numpy as np

from padvinder.util import normalize
from padvinder.util import check_finite

class Ray(object):
    """
    A ray consists of a starting position and a direction.
    Both are specified as vectors.

    The starting position is a point in the scene, the ray
    begins in. The direction is where the ray is heading
    in and is always normalized.

    Parameters
    ----------
    position : numpy.ndarray_like
        an array of three dimension
    direction : nump.ndarray_like
        Direction must have the same number of dimension as position. The
        direction vector will be stored normalized to a length of one and can
        not initially have lenght zero.

    Raises
    ------
    ValueError
        Raises a ValueError if the input contains NaNs or Infs.

    ZeroDivisionError
        Raises a ZeroDivisionError if the direction vector has length zero

    Examples
    --------
    >>> Ray((0, 0, 0), (1, 0, 0))
    Ray([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    >>> Ray((3.0, 2.3, -5.1), (-10.0, 34.0, -2.0))
    Ray([3.0, 2.3, -5.1], [-0.28171808,  0.95784149, -0.05634362])
    """
    def __init__(self,
                 position = (0,0,0),
                 direction = (1,0,0)
                 ):
        check_finite(position, direction)
        self._position = np.array(position).astype(np.float64)
        self._direction = normalize(direction).astype(np.float64)

    @property
    def position(self):
        """
        Return the ray's position.
        """
        return self._position

    @property
    def direction(self):
        """
        Return the ray's normalized direction.
        """
        return self._direction

    def point(self, distance):
        """
        Returns a point lying t-units from the origin on the ray.

        Parameters
        ----------
        distance : float
            The number of units along the ray to get the point of

        Returns
        -------
        point on ray : numpy.ndarray_like
            where the point is calculated as ray_origin + distance*ray_direction

        Examples
        --------
        >>> Ray((0, 0, 0), (1, 0, 0)).point(10)
        [10.0, 0.0, 0.0]
        """
        return self.position + distance*self.direction

    def __repr__(self):
        # converting the numpy array to string
        p, d = self.position, self.direction
        return "Ray({0}, {1})".format(p, d)
