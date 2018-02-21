#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Padvinder is the pathtracer / renderer that takes a scene and a camera and
produces an image.

.. moduleauthor:: Adrian Köring
"""

import numpy as np
import itertools as it

from padvinder.ray import Ray

class Padvinder(object):
    """
    Padvinder produces an image of a scene from the perspective of a camera.

    Rendersettings are passed in the constructor. To render the image, pass
    the scene and camera to the __call__ method.

    resolution : numpy.ndarray_like of shape (2, )
        The resolution of the output image

    sample_per_pixel : number
        The number of rays to trace per pixel - a higher number produces more
        noise free images

    path_length : number
        The number of intersections after which a path is terminated

    Example
    -------
    >>> padvinder = Padvinder()
    >>> image = padvinder(scene, camera)
    """
    def __init__(self, resolution = (100, 100),
                       sample_per_pixel = 5,
                       path_length = 2,
                       background_color = (0.1, 0.1, 0.1)):
        self._res_x, self._res_y = resolution
        self._spp = sample_per_pixel
        self._path_length = path_length
        self._bg_color = background_color

    @property
    def res_x(self):
        """
        Returns the resolution along the x-axis
        """
        return self._res_x

    @property
    def res_y(self):
        """
        Returns the resolution along the y-axis
        """
        return self._res_y

    @property
    def res(self):
        """
        Returns the resolution in both axis
        """
        return self.res_x, self.res_y

    @property
    def spp(self):
        """
        Return the Samples Per Pixel
        """
        return self._spp

    @property
    def path_length(self):
        """
        Return the number of intersections after which the path is terminated.
        """
        return self._path_length

    @property
    def background_color(self):
        """
        Return the background_color of the rendering.
        """
        return self._bg_color

    def __call__(self, scene, camera):
        """
        Kicks off the rendering and returns the image.

        scene : padvinder.scene.Scene
            The scene instance contains all the renderables to be rendered.

        camera : padvinder.camera.Camera
            The camera defines the viewpoint of the output image

        Returns
        -------
        rendered image : numpy.ndarray_like with shape (*resolution, 3)
            Returns the rendered image acquired by pathtracing the scene
            beginning from the camera.

        Example
        -------
        >>> padvinder = Padvinder()
        >>> image = padvinder(scene, camera)
        """
        self.scn = scene
        self.cam = camera

        img = np.zeros((self.res_x, self.res_y, 3))
        ray_permutations = range(self.spp), range(self.res_x), range(self.res_y)
        for (spp, px, py) in it.product(*ray_permutations):
            img[px, py] += self._trace(camera.ray((px, py), self.res), 0)

        return img / self.spp

    def _trace(self, ray, path_length):
        """
        Trace a given ray one step through the scene.

        ray : padvinder.ray.Ray
            the ray defining the direction and starting position to continue in

        path_length : number
            the number of intersections this path already had

        Returns
        -------
        color : numpy.ndarray_like of shape (3, )
            returns the light color flowing along the path
        """

        if path_length >= self.path_length:
            return np.zeros(3,)

        (t, obj) = self.scn.intersect(ray)

        if obj is None:
            return self.background_color

        point  = ray.point(t)
        normal = obj.normal(point)
        # to avoid numerical inaccuracies and the intersection point
        # ending up within an object
        point += 1e-4 * normal

        out_dir = obj.material.outgoing_direction(normal, ray.direction)

        color = self._trace(Ray(point, out_dir), path_length+1)

        # path tracing defined 'forward' direction
        # color accumulation, however, is backwards in <-> out
        return obj.material(normal, color, -out_dir, -ray.direction)
