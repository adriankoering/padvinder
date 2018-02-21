#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Materials define the surface properties and specify how light rays get coloured and reflected. All materials are callables - they implement the __call__ method
and can be used like functions.

.. moduleauthor:: Adrian Köring
"""

import numpy as np

from padvinder.util import normalize
from padvinder.util import check_finite

class Material(object):
    """
    An emission material consists of an emitted colour only.
    Without gradients, lighting or anything.

    Parameters
    ----------
    color : numpy.ndarray_like
        of three dimensions and contains colors as (Red, Green, Blue) where
        (0,0,0) is black and (1,1,1) is white

    Raises
    ------
    ValueError
        if the color contains any non-finite (inf, nan) values

    Examples
    --------
    >>> Material((0.8, 0.8, 0.8))
    Material(color=[.8 .8 .8])
    """
    def __init__(self, color = (.5, .5, .5)):
        check_finite(color)
        self._color = np.array(color).astype(np.float64)

    @property
    def color(self):
        """
        Returns the color of the material.
        """
        return self._color

    def __call__(self, surface_normal,
                       incoming_color,
                       incoming_direction,
                       outgoing_direction):
        """
        Calculate light reflected from the material toward the outgoing
        direction. Keep in mind, while pathtracing starts at the camera and
        heads into the scene, the rays contribution is accumulated 'backwards'.
        Therefore the incoming direction is further down the path and
        outgoing_direction is closer towards the camera.

        Parameters
        ----------
        surface_normal : numpy.ndarray_like
            normal vector at the geometries surface
        incoming_color : numpy.ndarray_like
            the color the ray has accumulated up to this point
        incoming_direction : numpy.ndarray_like
            the direction from where the 'light shines' onto the surface
        outgoing_direction : numpy.ndarray_like
            the direction into which the 'light gets reflected' from the surface

        Returns
        -------
        color : numpy.ndarray_like
            the light color 'getting reflected' from the surface
        """
        return self._color

    def __repr__(self):
        return "Material(color={})".format(self._color)


class Emission(Material):
    """
    Emission is equivalent to the abstract base class Material. Due to semantics
    this class exists and merely inherits without modifications.

    Parameters
    ----------
    color : numpy.ndarray_like
        of three dimensions and contains colors as (Red, Green, Blue) where
        (0,0,0) is black and (1,1,1) is white

    Raises
    ------
    ValueError
        if the color contains any non-finite (inf, nan) values

    Examples
    --------
    >>> Emission()
    Emission(color=[10.0, 10.0, 10.0])
    """
    def __init__(self, color = (10, 10, 10)):
        super().__init__(color)

    def __repr__(self):
        return "Emission(color={})".format(self._color)


class Lambert(Material):
    def __init__(self, color = (0.5, 0.5, 0.5), diffuse = 1):
        """
        A lambert material consists of a colour value and a diffuse coefficient.

        Parameters
        ----------
        color : numpy.ndarray_like
            of three dimensions and contains colors as (Red, Green, Blue) where
            (0,0,0) is black and (1,1,1) is white
        diffuse : number in [0, 1]
            percentage of incoming light that is reflected again

        Raises
        ------
        ValueError
            if the color contains any non-finite (inf, nan) values

        Examples
        --------
        >>> Lambert((0.8, 0.8, 0.8), 1)
        Lambert(color=[0.8, 0.8, 0.8], diffuse=1)
        """
        super().__init__(color)
        self._diffuse = diffuse

    @property
    def diffuse(self):
        """
        Returns the diffuse value of the material.
        """
        return self._diffuse

    def __call__(self, surface_normal,
                       incoming_light,
                       incoming_direction,
                       outgoing_direction):
        """
        Calculate light reflected from the material toward the outgoing
        direction. Keep in mind, while pathtracing starts at the camera and
        heads into the scene, the rays contribution is accumulated 'backwards'.
        Therefore the incoming direction is further down the path and
        outgoing_direction is closer towards the camera.

        Parameters
        ----------
        surface_normal : numpy.ndarray_like
            normal vector at the geometries surface
        incoming_color : numpy.ndarray_like
            the color the ray has accumulated up to this point
        incoming_direction : numpy.ndarray_like
            the direction from where the 'light shines' onto the surface
        outgoing_direction : numpy.ndarray_like
            the direction into which the 'light gets reflected' from the surface

        Returns
        -------
        color : numpy.ndarray_like
            the light color 'getting reflected' from the surface
        """
        raise NotImplemented()

    def __repr__(self):
        c, d = self._color, self._diffuse
        return "Lambert(color={0}, diffuse={1})".format(c, d)
