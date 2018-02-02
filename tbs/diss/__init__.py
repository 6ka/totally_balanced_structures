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

Submodules
----------

.. autosummary::
    :toctree:

    conversion
    file_io

Module content
--------------

"""

from .diss import Diss

__author__ = 'francois'

__all__ = ["conversion", "file_io", "Diss"]

