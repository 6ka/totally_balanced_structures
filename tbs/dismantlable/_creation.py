__author__ = "cchatel", "fbrucker"

import random

from ._dismantlable_lattice import DismantlableLattice
from ..graph import DirectedGraph


def random_dismantlable_lattice(n_vertices, top="TOP", bottom="BOTTOM", new_vertex=lambda lattice: len(lattice)):
    """Create a random dimantlable lattice.

    Iteratively add a doubly irreducible element to an original 2-element lattice.

    Args:
        n_vertices(int): the number of vertices (excluding bottom and top)
        top: the top element
        bottom: the bottom element
        new_vertex(lattice -> element): a new element.

    Returns(DismantlableLattice): a random dismantlable lattice.
    """

    crown_free = DismantlableLattice(DirectedGraph([bottom, top], [(bottom, top)]))

    all_elements = [bottom]
    for step in range(n_vertices):
        element = new_vertex(crown_free)

        u = random.sample(all_elements, 1)[0]
        v = random.sample(crown_free.upper_filter(u) - {u}, 1)[0]
        crown_free.add_join_irreducible(element, u, v)
        all_elements.append(element)

    return crown_free
