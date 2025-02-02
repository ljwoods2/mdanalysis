# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- https://www.mdanalysis.org
# Copyright (c) 2006-2017 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the Lesser GNU Public Licence, v2.1 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler,
# D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein.
# MDAnalysis: A Python package for the rapid analysis of molecular dynamics
# simulations. In S. Benthall and S. Rostrup editors, Proceedings of the 15th
# Python in Science Conference, pages 102-109, Austin, TX, 2016. SciPy.
# doi: 10.25080/majora-629e541a-00e
#
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#

"""\
Set box dimensions --- :mod:`MDAnalysis.transformations.boxdimensions`
=======================================================================

Set dimensions of the simulation box, either to a constant vector across
all timesteps or to a specified vector at each frame.

.. autoclass:: set_dimensions
"""
import numpy as np

from .base import TransformationBase


class set_dimensions(TransformationBase):
    """
    Set simulation box dimensions.

    Timestep dimensions are modified in place.

    Examples
    --------

    e.g. set simulation box dimensions to a vector containing unit cell
    dimensions [*a*, *b*, *c*, *alpha*, *beta*, *gamma*], lengths *a*,
    *b*, *c* are in the MDAnalysis length unit (Å), and angles are in degrees.
    The same dimensions will be used for every frame in the trajectory.

    .. code-block:: python

        dim = np.array([2, 2, 2, 90, 90, 90])
        transform = mda.transformations.boxdimensions.set_dimensions(dim)
        u.trajectory.add_transformations(transform)

    Or e.g. set simulation box dimensions to a vector containing unit cell
    dimensions [*a*, *b*, *c*, *alpha*, *beta*, *gamma*] at the first frame,
    and [*2a*, *2b*, *2c*, *alpha*, *beta*, *gamma*] at the second frame.

    .. code-block:: python

        dim = np.array([
            [2, 2, 2, 90, 90, 90],
            [4, 4, 4, 90, 90, 90],
        ])
        transform = mda.transformations.boxdimensions.set_dimensions(dim)
        u.trajectory.add_transformations(transform)

    Parameters
    ----------
    dimensions: iterable of floats or two-dimensional np.typing.NDArrayLike
        vector that contains unit cell lengths and angles.
        Expected shapes are (6, 0) or (1, 6) or (N, 6), where
        N is the number of frames in the trajectory. If shape is (6, 0) or
        (1, 6), the same dimensions will be used at every frame in the
        trajectory.

    Returns
    -------
    :class:`~MDAnalysis.coordinates.timestep.Timestep` object


    .. versionchanged:: 2.7.0
       Added the option to set varying box dimensions (i.e. an NPT trajectory).
    """

    def __init__(self, dimensions, max_threads=None, parallelizable=True):
        super().__init__(
            max_threads=max_threads, parallelizable=parallelizable
        )
        self.dimensions = dimensions

        try:
            self.dimensions = np.asarray(self.dimensions, np.float32)
        except ValueError:
            errmsg = (
                f"{self.dimensions} cannot be converted into "
                "np.float32 numpy.ndarray"
            )
            raise ValueError(errmsg)
        try:
            self.dimensions = self.dimensions.reshape(-1, 6)
        except ValueError:
            errmsg = (
                f"{self.dimensions} array does not have valid box "
                "dimension shape.\nSimulation box dimensions are "
                "given by an float array of shape (6, 0), (1, 6), "
                "or (N, 6) where N is the number of frames in the "
                "trajectory and the dimension vector(s) containing "
                "3 lengths and 3 angles: "
                "[a, b, c, alpha, beta, gamma]"
            )
            raise ValueError(errmsg)

    def _transform(self, ts):
        try:
            ts.dimensions = (
                self.dimensions[0]
                if self.dimensions.shape[0] == 1
                else self.dimensions[ts.frame]
            )
        except IndexError as e:
            raise ValueError(
                f"Dimensions array has no data for frame {ts.frame}"
            ) from e
        return ts
