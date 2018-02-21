#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
A Scene is a collection of renderables and performs intersection tests on every
contained object.

.. moduleauthor:: Adrian Köring
"""

import numpy as np

class Scene(object):
    """
    A scene contains a collection of renderable objects and performs ray
    intersections on them. Eventually the distance to the intersection point
    and the intersected object are returned. If no renderable was intersected
    (np.inf, None) is returned.

    Parameters
    ----------
    renderable : padvinder.geometry.Geometry
        and subclasses. A renderable has to implement the intersect(ray) method
    """
    def __init__(self, *renderable):
        self._renderable = list(renderable)

    def __iter__(self):
        return iter(self._renderable)

    def intersect(self, ray):
        """
        Performs intersection tests with every renderable in the scene.

        Parameters
        ----------
        ray : Ray
            the light ray to trace through the scene
            has to support ray.position and ray.direction

        Returns
        -------
        (number, renderable) : (float, padvinder.geometry.Geometry)
            Number is a float in the intervall of [0, np.inf] and corresponds to
            the distance along the ray to the intersection point on the
            renderable surface. The renderable is an object previously passed
            into the scene that was intersected by the ray. If multiple
            renderables are intersected in the Scene, the one with the shortest
            distance between intersection point and ray position is returned.
            If no intersection occured **(np.inf, None)** is returned.
        """
        out_dist = np.inf
        out_obj = None

        for obj in self:
            dist = obj.intersect(ray)
            if dist < out_dist:
                out_dist = dist
                out_obj  = obj

        return out_dist, out_obj
