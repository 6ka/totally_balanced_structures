""" Dissimilarity module.

.. currentmodule:: tbs.diss

Data described by a :class:`Diss` can be real (real numbers), intervals (values are subset), or whatever suits
the application.


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


Module content
--------------

"""

from .diss import Diss
from .order import min, max, rank
from .file_io import load, save

__author__ = 'francois'

__all__ = ["Diss", "min", "max", "rank", "load", "save"]

