import numpy as np

from padvinder.util import normalize
from padvinder.util import check_finite

class Ray:
    def __init__(self,
                 position = (0,0,0),
                 direction = (1,0,0)
                 ):
        """
        A ray consists of a starting position and a direction.
        Both are specified as vectors.

        The starting position is a point in the scene, the ray
        begins in. The direction is where the ray is heading
        in and is always normalized.

        Parameters
        ----------
        origin : nd-array of three dimension
        direction : nd-array
            Direction must have the same dimension as origin or vice versa.
            Direction will be stored normalized.
            Direction can not have length zero.

        Returns
        -------
        ray : Ray
            with the given position and direction.

        Errors
        ------
        ValueError : Raises a ValueError if the direction vector is of
            length zero, or the input contains NaNs or Infs.

        Examples
        --------
        >>> ray((0, 0, 0), (1, 0, 0))
        ray([0 0 0], [1 0 0])
        >>> ray((3.0, 2.3, -5.1), (-10, 34, -2))
        ray([3.0, 2.3, -5.1], [-0.28171808,  0.95784149, -0.05634362])
        """
        check_finite(position, direction)
        self._position = np.array(position).astype(np.float64)
        self._direction = normalize(direction).astype(np.float64)


    @property
    def position(self):
        """
        Return the vector's position.
        """
        return self._position

    @property
    def direction(self):
        """
        Return the vector's normalized direction.
        """
        return self._direction

    def point(self, distance):
        """
        Returns a point lying t-units from the origin on the ray.

        Parameters
        ----------
        distance : number
            The number of units along the ray to get the point of

        Returns
        -------
        np-array : n-dimensional arry
            ray_origin + distance*ray_direction

        Examples
        --------
        ray((0, 0, 0), (1, 0, 0)).point(10) = [10 0 0]
        """
        return self.position + distance*self.direction

    def __str__(self):
        # converting the numpy array to string
        p, d = self.position, self.direction
        return "Ray({0}, {1})".format(p, d)
