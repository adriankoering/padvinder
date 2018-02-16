# """
# .. module:: Material
#    :synopsis: Materials define the surface properties of an geometric object.
# """

import numpy as np

from padvinder.util import normalize
from padvinder.util import check_finite

class Material(object):
    """
    An emission material consists of an emitted colour only.
    Without gradients, lighting or anything.

    Parameters
    ----------
    color : nd-array of three or four dimensions
             3d contains (Red, Green, Blue) - (RGB)
             (0,0,0) is black, (1,1,1) is white

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
        return self._color

    def __call__(self, surface_position,
                       surface_normal,
                       incoming_light,
                       incoming_direction,
                       outgoing_direction):
        return self._color

    def __repr__(self):
        return "Material(color={})".format(self._color)


class Emission(Material):
    """
    Emission is structurally equivalent to the base-material,
    but due to semantics it inherits and is not itself the
    base-class - not every material is an emitter.
    """
    def __repr__(self):
        return "Emission(color={})".format(self._color)


class Lambert(Material):
    def __init__(self, color = (0.5, 0.5, 0.5), diffuse = 1):
        """
        A lambert material consists of a colour value and a diffuse coefficient.

        Parameters
        ----------
        color : nd-array of three dimensions
            3d contains (Red, Green, Blue) - (RGB)
        diffuse : number in [0, 1]
            percentage of incoming light that is reflected again

        Examples
        --------
        >>> Lambert((0.8, 0.8, 0.8), 1)
        Lambert([.8 .8 .8], 1)
        """
        super().__init__(color)
        self._diffuse = diffuse

    @property
    def diffuse(self):
        return self._diffuse

    def __repr__(self):
        c, d = self._color, self._diffuse
        return "Lambert(color={0}, diffuse={1})".format(c, d)

    def __call__(self, surface_position,
                       surface_normal,
                       incoming_light,
                       incoming_direction,
                       outgoing_direction):
        raise NotImplemented()
