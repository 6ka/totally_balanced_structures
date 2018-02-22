__author__ = 'cchatel', 'fbrucker'

__all__ = ["isa_lattice_cover_graph"]

from .. import graph


def isa_lattice_cover_graph(cover_graph):
    """True if *graph* is the cover graph of a lattice order.

    Args:
        graph: directed graph.

    returns(bool):
        True if graph is the covergraph of a lattice order, False otherwise.
    """

    order = graph.topological_sort(cover_graph)
