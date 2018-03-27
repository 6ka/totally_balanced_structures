__author__ = "cchatel", "fbrucker"

import random

from ._dismantlable_lattice import DismantlableLattice
from ..graph import DirectedGraph


def random_dismantlable_lattice(vertices, bottom="BOTTOM", top="TOP"):
    """Create a random dimantlable lattice.

    Iteratively add a doubly irreducible element to an original 2-element lattice.

    Args:
        top: the top element
        bottom: the bottom element
        vertices(iterable): the non top/bottom lattice elements.

    Returns(DismantlableLattice): a random dismantlable lattice.
    """

    crown_free = DismantlableLattice(DirectedGraph([bottom, top], [(bottom, top)]))

    all_elements = [bottom]
    for element in vertices:

        u = random.sample(all_elements, 1)[0]
        v = random.sample(crown_free.above_filter(u) - {u}, 1)[0]
        crown_free.add_join_irreducible(element, u, v)
        all_elements.append(element)

    return crown_free
