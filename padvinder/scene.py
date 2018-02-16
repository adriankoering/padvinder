# """
# .. module:: Scene
#    :synopsis: A scene performs intersection tests on every renderable object.
# """

import numpy as np

class Scene(object):
    def __init__(self, *renderable):
        """
        A scene gathers a collection of renderable objects and performs ray intersections on them
        """
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
        (number, renderable) where
            number is in [0, np.inf] - the distance along the ray to the
            object surface and renderable is an object previously passed into
            the scene that is intersected by the ray with the shortest distance.
        """
        out_dist = np.inf
        out_obj = None

        for obj in self:
            dist = obj.intersect(ray)
            if dist < out_dist:
                out_dist = dist
                out_obj  = obj

        return out_dist, out_obj
