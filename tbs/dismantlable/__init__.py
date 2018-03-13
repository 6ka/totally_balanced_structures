""" Dismantlable module.

.. currentmodule:: tbs.dismantlable


Module content
--------------

"""



__author__ = 'cchatel', 'fbrucker'

__all__ = ["DismantlableLattice", "random_dismantlable_lattice", "tree_decomposition_of_binary_lattice"]

from ._dismantlable_lattice import DismantlableLattice
from ._creation import random_dismantlable_lattice
from ._tree_decomposition import tree_decomposition_of_binary_lattice
