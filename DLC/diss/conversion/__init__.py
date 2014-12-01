"""Convert :class:`CTK.diss.Diss` to various types.

.. currentmodule:: CTK.diss.conversion

Module content
--------------

.. autosummary::
    :toctree:

    to_string
    to_graph
"""

__author__ = 'francois'
__all__ = ["to_string", "to_graph"]

from .to_string import to_string
from .to_graph import to_graph
