"""Context Matrix.

.. currentmodule:: context_matrix

Glossary
--------

.. glossary::

    context maxtrix
        0/1 matrix each line is an element and each column an attribute.


Submodules
----------

.. autosummary::
    :toctree:

    file_io


Module content
--------------

.. autosummary::
    :toctree:

    ContextMatrix
    to_string

"""

__author__ = 'francois'

__all__ = ["ContextMatrix", "to_string", "file_io"]

from .context_matrix import ContextMatrix
from .to_string import to_string