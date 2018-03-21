"""Context Matrix.

.. currentmodule:: tbs.contextmatrix

Glossary
--------

.. glossary::

    context maxtrix
        0/1 matrix each line is an element and each column an attribute.


Module content
--------------

"""

from ._context_matrix import ContextMatrix
from ._to_string import to_string
from ._file_io import load, save

__author__ = 'francois'

__all__ = ["ContextMatrix", "load", "save", "to_string"]



