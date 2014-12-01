"""Generic Dissimilarity module.

.. currentmodule:: CTK.diss

Since :class:`CTK.diss.Diss` only assumes the symmetry, one can create
dissimilarities not taking their values in real numbers (`2^X` for instance) and
even having different values for d(x, x). Nevertheless, most of the methods
described in this module require *real* dissimilarities and do not consider
d(x, x) values (they are supposed to be equal to 0).

Glossary
--------

.. glossary::

    dissimilarity
        Given a set X, a *dissimilarity* d is symmetric function from XxX to
        the set of real numbers, and d(x, x) = 0 for all x in X.

    dissimilarities
        see :term:`dissimilarity`.

    real dissimilarity
        A dissimilarity taking their values from the set of real numbers.

Submodules
----------

.. autosummary::
    :toctree:

    conversion
    file_io

Module content
--------------

.. autosummary::
    :toctree:

    Diss
"""

__author__ = 'francois'

__all__ = ["conversion", "file_io", "Diss"]

from .diss import Diss