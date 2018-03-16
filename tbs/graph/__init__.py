"""Generic Graph module.

.. currentmodule:: tbs.graph


We assume that edges are subsets of `X`. In its
whole generality, one can just supposes that `E` is a set of two element
tuples. Such graph are said to be *directed*. That is if  `(x, y)` is an edge,
`(y, x)` is not necessarily one. It is possible to produce directed graphs in
:mod:`base` but most of the methods and functions handle only nondirected graphs.

Glossary
--------

.. glossary::

    graph
        Given a set X, a *graph* G is a couple (X, E) where E is a set of two element subsets
        of X.

    graphs
        See :term:`graph`.

    vertex
        Given a graph G = (X, E), X is said to be the *vertices* of G.

    vertices
        See vertex.

    edge
        Given a :term:`graph` G = (X, E), E is said to be the *edges* of G.

    edges
        See :term:`edge`.

    directed graph
        Given a set `X`, a *graph* `G` is a couple (X, E) where E is a set of two element tuple
        of `X`.

Module content
--------------

"""

from ._mixed_graph import MixedGraph, UNDIRECTED_EDGE, DIRECTED_EDGE
from ._graph import cls
from ._directed_graph import DirectedGraph

from ._connected_parts import mst_from_set, connected_parts
from ._order import dfs, bfs, topological_sort, \
    direct_acyclic_graph_to_direct_comparability_graph, direct_comparability_graph_to_hase_diagram


__author__ = 'francois'

__all__ = ["cls",
           "DirectedGraph",
           "mst_from_set", "connected_parts",
           "MixedGraph", "UNDIRECTED_EDGE", "DIRECTED_EDGE",
           "mst_from_set", "dfs", "bfs", "topological_sort",
           "direct_acyclic_graph_to_direct_comparability_graph", "direct_comparability_graph_to_hase_diagram"]

