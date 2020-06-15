""" Lehelian totally balanced hypergraphs.

.. currentmodule:: tbs.lehelian

    Lehelian totally balanced hypergraphs are totally balanced hypergraphs with maximal number of clusters. A
    lehelian hypergraph with n vertices has (2 n+1) clusters.


Module content
--------------

"""

from ._creation import random_lehelian_hypergraph

__author__ = 'francois, célia'

__all__ = ["random_lehelian_hypergraph"]
