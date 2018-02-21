#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Module collecting a number of renderable objects. Geometry is an abstract base
class defining the interface and Sphere and Plane are concrete, renderable
implementatons.

.. moduleauthor:: Adrian Köring
"""

import numpy as np

from padvinder.util import normalize
from padvinder.util import check_finite

from padvinder.ray      import Ray
from padvinder.material import Material

class Geometry(object):
    """
    Baseclass for geometry. Either implicitly
    (eg. spheres and planes) or explicitly via triangles.

    Parameters
    ----------
    material : padvinder.material.Material
        A material specifies how the geometry surface interacts with light rays

    Examples
    --------
    >>> Geometry()
    Geometry(Material(color=[0.5, 0.5, 0.5]))
    """
    def __init__(self, material = Material()):
        self._material = material

    @property
    def material(self):
        """
        Returns the material of this geometry instance.
        """
        return self._material

    def intersect(self, ray):
        """
        Given a ray, intersect it with this geometry instance and
        returns the distance t of ray position to intersection point
        (so that ray.point(t) is the intersection point)
        If no intersection occurs +inf is returned.

        Parameters
        ----------
        ray : Ray
            the ray to be tested for intersection

        Returns
        -------
        float
            in (0, +inf]

        Raises
        ------
        NotImplemented
            because this is an abstract base class

        Examples
        --------
        >>> a = Sphere()
        >>> r = Ray()
        >>> a.intersect(r)
        1.0
        """
        raise NotImplemented()

    def normal(self, x):
        """
        Given a point on the surface of the geometry instance and
        returns the surface normal at that point.

        Parameters
        ----------
        x : numpy.ndarray_like
            point on the geometry instance

        Returns
        -------
        n : numpy.ndarray_like
            normal vector of the geometry surface at this point

        Raises
        ------
        NotImplemented
            because this is an abstract base class
        """
        raise NotImplemented()

    def __repr__(self):
        return "Geometry({0})".format(self._material)


class Sphere(Geometry):
    """
    An implicitly modeled sphere is given by:
        LA.norm(position - x) - r = 0,
        where position is the center of the sphere,
        x is a point on the surface of the sphere and
        r is the radius.

    Parameters
    ----------
    material : padvinder.material.Material
        A material specifies how the geometry surface interacts with light rays
    position : numpy.ndarray_like
        position of the sphere's center in world coordinates
    radius : number
        radius of the sphere

    Examples
    --------
    >>> Sphere() #unitsphere
    Sphere(Material(color=[0.5, 0.5, 0.5]),
                    position=[0.0, 0.0, 0.0],
                    radius=1)
    """
    def __init__(self, material = Material(),
                       position = (0,0,0),
                       radius   = 1):
        super().__init__(material)
        check_finite(position, radius)
        self._position = np.array(position).astype(np.float64)
        self._radius = radius

    @property
    def position(self):
        """
        Returns the position of the center of the sphere.
        """
        return self._position

    @property
    def radius(self):
        """
        Returns the radius of the sphere.
        """
        return self._radius

    def intersect(self, ray):
        """
        Given a ray, intersect it with this sphere instance and
        returns the distance t of ray position to intersection point
        (so that ray.get_point(t) is the intersection point)
        If no intersection occurs +inf is returned.

        Parameters
        ----------
        ray : Ray
            the ray to be tested for intersections

        Returns
        -------
        float
            number in (0, +inf]
        """
        # a = 1 = ray.d @ ray.d
        tmp = ray.position - self.position
        b = np.dot(2*tmp, ray.direction)
        c = np.dot(tmp, tmp) - self.radius**2
        disc = b**2  - 4*c # /a is ommitted, because it is 1
        if disc > 0:
            disc = np.sqrt(disc)
            q = (-b - disc) / 2 if b < 0 else (-b + disc) / 2
            t0 = q
            t1 = c/q
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0
        return np.inf

    def normal(self, x):
        """
        Given a point on the surface of the sphere instance and
        returns the surface normal at that point.

        Parameters
        ----------
        x : numpy.ndarray_like
            point on the geometry instance

        Returns
        -------
        normal : numpy.ndarray_like
            normal vector of the geometry surface at this point
        """
        return normalize(x - self.position)

    def __repr__(self):
        m, p, r = self.material, self.position, self.radius
        return "Sphere({0}, position={1}, radius={2})".format(m, p, r)


class Plane(Geometry):
    """
    An implicitly modelled plane is given by n * x - d = 0,
    where n is the normal vector, x is a point in world coordinates,
    d is a number and n * x is the dot product of two vectors.

    Parameters
    ----------
    material : padvinder.material.Material
        material instance
    position : numpy.ndarray_like
        the 'origin' of the plane - any point in the world the plane passes through
    normal : numpy.ndarray_like
        the normalised vector thats orthogonal to the plane

    Examples
    --------
    >>> Plane()   # equivalent to ...
    >>> Plane(Material(), (0, 0, 0), (1, 0, 0))
    Plane(Material(color=[1., 1., 1.]), position=(0, 0, 0), normal=(0, 1, 0))
    """
    def __init__(self, material=Material(),
                       position=(0,0,0),
                       normal=(0,1,0)):
        super().__init__(material)
        check_finite(position, normal)
        self._position = np.array(position, dtype="float")
        self._normal = normalize(np.array(normal))

    @property
    def position(self):
        """
        Returns the position of the plane.
        """
        return self._position

    def intersect(self, ray):
        """
        Given a ray
        Returns the value t so that ray.get_point(t) is the closest
        intersection point or +inf if the plane is not hit.

        Parameters
        ----------
        ray : Ray
            the ray to be tested for intersections

        Returns
        -------
        number in (0, +inf]

        Examples
        --------
        >>> a = plane()
        >>> r = ray()
        >>> a.intersect(r)
        1.0
        """
        d  = np.dot(ray.direction, self._normal)
        if np.abs(d) > 1e-8:
            d = np.dot((self.position - ray.position), self._normal) / d
            return d if d > 0 else np.inf
        return np.inf

    def normal(self, x):
        """
        Given a point on the surface of the plane,
        returns the surface normal at that point.

        Parameters
        ----------
        x : numpy.ndarray_like
            point on the plane instance

        Returns
        -------
        normal : numpy.ndarray_like
            normal vector of the plane surface at this point
        """
        return self._normal

    def __repr__(self):
        m, p, n = self._material, self._position, self._normal
        return "Plane({0}, position={1}, normal={2})".format(m, p, n)
