import numpy as np

from padvinder.util import normalize

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
        self._check_input(position, direction)
        self._p = np.array(position).astype(np.float64)
        self._d = normalize(direction).astype(np.float64)

    def _check_input(self, position, direction):
        """
        Validate the input parameters and raise ValueErrors if incompatible
        values are present.
        """
        if    (not np.isfinite(position).all()
            or not np.isfinite(direction).all()):
            raise ValueError("Input to Ray({}, {})".format(position, direction)
                            + " can not contain Inf or NaN")

    @property
    def p(self):
        """
        Return the vector's position.
        """
        return self._p

    @property
    def d(self):
        """
        Return the vector's normalized direction.
        """
        return self._d

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
        return self._p + distance*self._d

    def __str__(self):
        # converting the numpy array to string
        return "Ray({0}, {1})".format(self._p, self._d)
