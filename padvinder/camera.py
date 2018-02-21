#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Cameras produce the initial ray from the camera position through the currently
rendered pixel and into the scene.

.. moduleauthor:: Adrian Köring
"""

import numpy as np
from padvinder.ray  import Ray
from padvinder.util import normalize
from padvinder.util import check_finite

class Camera(object):
    """
    This Camera Model sets up and contains an orthonormal coordinate
    system. The cameras position is the starting positon of all rays fired
    into the scene. The rays through the center of the image will pass
    through the look_at point. Position and look_at define the optical axis.
    The up vector provides a vague upwards direction helping to orient the
    camera.

    Parameters
    ----------
    position : numpy.ndarray_like
        the position of the camera in the scene, origin of the fired rays
    up : numpy.ndarray_like
        the general upwards direction of the camera
    look_at : numpy.ndarray_like
        the position in the scene that the camera will look at

    Raises
    ------
    ValueError
        if any of position, up or look_at contain Infs or NaNs
        or if the position and look_at are at the same point

    Examples
    --------
    >>> Camera()
    >>> Camera((0,0,0), (0,1,0), (0,0,-1), 35)
    Camera(position=[0.0, 0.0, -1.0],
           up=[0.0, 1.0, 0.0],
           look_at=[0.0, 0.0, 0.0])
    """
    def __init__(self,
                 position = (0,0,0),
                 up       = (0,1,0),
                 look_at  = (0,0,1)):
        check_finite(position, up, look_at)
        if np.isclose(position, look_at).all():
            raise ValueError("Position and look_at of a Camera can not be "
                            + "the same point, move either one away")

        self._position = np.array(position, dtype=np.float64)
        self._optical_axis = None
        self._righthand    = None
        self._up           = None
        self._build_coordinate_system(up, look_at - self._position)

    def _build_coordinate_system(self, vague_up, optical_axis):
        """
        Given the rough user specified setup of a camera,
        create an orthonormal coordinate system.

        Parameters
        ----------
        vague_up : numpy.ndarray_like
            the general upwards direction of the camera.
        optical_axis : numpy.ndarray_like
            the direction in which the optical axis of the camera points - will
            be orthongonal to the image plane.
        """
        vague_up = normalize(vague_up)

        self._optical_axis = normalize(optical_axis)
        self._righthand = np.cross(vague_up, self._optical_axis)
        self._up = np.cross(self._optical_axis, self._righthand)

    @property
    def position(self):
        """
        Return the position of the camera.
        """
        return self._position

    @property
    def up(self):
        """
        Return the up vector of the camera.
        """
        return self._up

    @property
    def optical_axis(self):
        """
        Return the optical axis of the camera.
        """
        return self._optical_axis

    def ray(self, pixel, dimensions, rand = True):
        """
        Given the pixel and the camera resolution, returns a ray that
        originates at the camera position and passes
        through the pixel. If rand is set true, a little random offset (smaller
        than the distance between two pixels is added to the pixel position.
        This will together with multiple samples per pixel mitigate aliasing.

        Parameters
        ----------
        pixel : numpy.ndarray_like
            (x, y) coordinates of the pixel in the image - numpy style. Aka
            (0, 0) is the upper left hand corner and the x values are iterating
            downwards while y is iterating horizontally.
            x must be in the intervall of [0, dimension[0]]
            and y must be in [0, dimension[1]]
            The pixel [0,0] is the upper lefthand corner and the
            pixel [res_x, rex_y] is the lower righthand corner.
        dimensions : numpy.ndarray_like
            (res_x, resx_y) the resolution of the camera in x and y.
        rand : boolean
            When False, every ray passes through the exact center of
            the pixel. When True a random offset smaller than the distance
            between two pixels is added the the pixel center. The ray then
            passes through the perturbed pixel center.

        Returns
        -------
        ray : Ray
            with the position being the camera position
            and direction being a vector that starts at the position
            and passes through the (potentiall offsetted) given pixel

        Raises
        ------
        NotImplemeted
            because this is an abstract base class
        Examples
        --------
        >>> camera = PerspectiveCamera()
        >>> camera.ray((0,0), (100, 100), False)
        """
        raise NotImplemented()

    def __repr__(self):
        return "Camera(position={}, ".format(self._position) \
                + "up={}, ".format(self._up) \
                + "optical axis={})".format(self._optical_axis)


class PerspectiveCamera(Camera):
    """
    The Perspective Camera Model extends the orthonormal coordinate
    system with a focal length and therefore a concrete image plane.
    The cameras position is the starting positon of all rays fired
    into the scene. The rays through the center of the image will pass
    through the look_at point. Position and look_at define the optical
    axis. The up vector provides a vague upwards direction helping to
    orient the camera. The focal length defines how far the 35mm
    equivalent sized image plane is from the camera position.

    Parameters
    ----------
    position : numpy.ndarray_like
        the position of the camera in the scene, origin of the fired rays
    up : numpy.ndarray_like
        the general upwards direction of the camera
    look_at : numpy.ndarray_like
        the position in the scene that the camera will look at
    focal_length : float
        the distance in mm between the position and the image plane -
        must be in the intervall of (0, +inf).

    Raises
    ------
    ValueError
        if any of position, up or look_at contain Infs or NaNs
        or if the position and look_at are at the same point
        of ir the focal_length is not positive

    Examples
    --------
    >>> PerspectiveCamera()
    >>> PerspectiveCamera((0,0,1), (0,1,0), (0,0,0), 24)
    Camera(position=[0.0, 0.0, 1.0],
           up=[0.0, 1.0, 0.0],
           look_at=[0.0, 0.0, 0.0],
           focal_length=24)
    """
    def __init__(self,
                 position = (0,0,0),
                 up       = (0,1,0),
                 look_at  = (0,0,1),
                 focal_length = 24):

        super().__init__(position, up, look_at)
        if focal_length <= 0:
            raise ValueError("Focal length must be larger than zero")

        self._focal_length = focal_length
        self._image_plane_center = (self.position
                                  + (self.focal_length/24.) * self.optical_axis)

    @property
    def focal_length(self):
        """
        Return the focal length of the camera.
        """
        return self._focal_length

    def ray(self, pixel, dimensions, rand = True):
        """
        Given the pixel and the camera resolution, returns a ray that
        originates at the camera position and passes
        through the pixel. If rand is set true, a little random offset (smaller
        than the distance between two pixels is added to the pixel position.
        This will together with multiple samples per pixel mitigate aliasing.

        Parameters
        ----------
        pixel : numpy.ndarray_like of shape (2, )
            (x, y) coordinates of the pixel in the image. Numpy style: aka
            (0, 0) is the upper left hand corner and the x values are iterating
            downwards while y is iterating horizontally.
            x must be in the intervall of [0, dimension[0]]
            and y must be in [0, dimension[1]]
            The pixel [0,0] is the upper lefthand corner and the
            pixel [res_x, rex_y] is the lower righthand corner.
        dimensions : numpy.ndarray_like of shape (2, )
            the resolution of the camera in x and y.
        rand : boolean
            When False, every ray passes through the exact center of
            the pixel. When True a random offset smaller than the distance
            between two pixels is added the the pixel center. The ray then
            passes through the perturbed pixel center.

        Returns
        -------
        ray : Ray
            with the position being the camera position
            and direction being a vector that starts at the position
            and passes through the (potentiall offsetted) given pixel

        Examples
        --------
        >>> camera = PerspectiveCamera()
        >>> camera.ray((50, 50), (100, 100), False)
        Ray(position=[0, 0, 0], direction=[0, 0, 1])
        """
        pixel_x, pixel_y = pixel
        dim_x, dim_y = dimensions
        max_dim = np.maximum(dim_x, dim_y)

        # image plane coordinates (x, y) of the pixel
        # x and y are in [-1, 1]
        x = (dim_x - 2*pixel_x) / max_dim
        y = (dim_y - 2*pixel_y) / max_dim

        if rand:
            # add a small perturbation to the pixel coordinate
            delta_x, delta_y = 1/dim_x, 1/dim_y
            sample_x, sample_y = np.random.uniform(-1, 1, size=(2,))
            x += sample_x * delta_x
            y += sample_y * delta_y

        world_coord = self._image_plane_center + x*self._righthand + y*self._up
        return Ray(self._position, world_coord - self._position)


    def __repr__(self):
        return ("PerspectiveCamera(position={}, ".format(self._position)
                + "up={}, ".format(self._up)
                + "optical axis={}, ".format(self._optical_axis)
                + "focal length={})".format(self._focal_length))
