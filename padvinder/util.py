import numpy as np
import numpy.linalg as LA

"""
A number of frequently used functions in various parts of rendering.
"""


def normalize(arr):
    """
    Returns a normalized version of the provided vector.

    Parameters
    ----------
    arr : nd-array
        The nd-array to be normalized.
        The original data type is returned, if the datatype supports the
        division-operator.
        Else a numpy array with the normalized vector will be returned.

    Returns
    -------
    provided data type or nd-array : n-dimensional array

    Errors
    ------
    RuntimeWarning : if the length of the provided nd-array is zero
        the division by zero causes a RuntimeWarning to be raised

    Examples
    --------
    >>> normalize([2,4,4])
    [ 0.33333333  0.66666667  0.66666667]
    >>> normalize(np.array((3,4,5)))
    [ 0.42426407  0.56568542  0.70710678]
    ### np.linalg.norm(normalize((x, y, z))) ~= 1
    """
    norm = LA.norm(arr)
    if norm < 1e-8:
        raise ZeroDivisionError("division by zero")
    return arr / LA.norm(arr)
