#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Utilities contains a number of frequently used functions.
"""

import numpy as np
import numpy.linalg as LA


def normalize(array):
    """
    Returns a normalized version of the provided array.

    Parameters
    ----------
    array : numpy.ndarray_like
        The array to be normalized. Afterwards np.linalg.norm(normalize(array))
        is approximately equal to 1.

    Returns
    -------
    normalized array : numpy.ndarray_like
        the array normalized to unit length:
        np.linalg.norm(normalize(array)) ~= 1.

    Raises
    ------
    ValueError
        if the input array contains Inf's or Nan's
    ZeroDivisionError
        if the length of the provided array has length ofzero the division will
        cause a ZeroDivisionError to be raised

    Examples
    --------
    >>> normalize([1, 0, 0])
    [1.0, 0.0, 0.0]
    >>> normalize([2, 4, 4])
    [0.33333333, 0.66666667, 0.66666667]
    >>> normalize(np.array((3,4,5)))
    [0.42426407, 0.56568542, 0.70710678]
    ### np.linalg.norm(normalize((x, y, z))) ~= 1
    """
    if not np.isfinite(array).all():
        raise ValueError("Can not normalize array {}".format(array)
                        + "because it contains NaN or Inf")
    norm = LA.norm(array)
    if norm < 1e-9:
        raise ZeroDivisionError("Division by zero")
    return array / norm


def check_finite(*args):
    """
    Validate the input parameters and raise ValueErrors if any contains
    incompatible values (Infs or NaNs) are present.

    Parameters
    ----------
    args : numpy.ndarray_like
        a list of lists or arrays

    Raises
    ------
    ValueError
        if any passed in element is Inf or NaN.
    """
    for e in args:
        if not np.isfinite(e).all():
            raise ValueError("Input was {}".format(e)
                            + ", but can not contain Inf or NaN")
