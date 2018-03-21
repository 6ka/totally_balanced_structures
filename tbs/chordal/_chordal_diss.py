from ._chordal_order import chordal_order
from ._order_finder import has_order_by_map
from ..diss import Diss


def isa_chordal_diss(diss):
    """ Check whether the dissimilarity is chordal or not.

    If the dissimilarity is not chordal, returns a good approximation.

    Args:
        diss(Diss):

    Returns(bool): True if diss is chordal, False otherwise.

    """
    return has_order_by_map(diss, lambda x, y, z: diss(y, z) > max(diss(x, y), diss(x, z)) and 1 or 0)


def approximate_to_chordal_diss(diss_orig, order=None):
    """ Return a chordal dissimilarity.

    Args:
        diss (Diss):
        order (list): vertex order. If None, a good approximation order is found.

    Returns (Diss): an approximated dissimilarity.

    """
    diss = Diss(diss_orig).update(diss_orig)

    if order is None:
        order = chordal_order(diss)

    for i in range(len(order)):
        for j in range(i, len(order)):
            for k in range(j, len(order)):
                if diss(order[j], order[k]) > max(diss(order[i], order[j]), diss(order[i], order[k])):
                    diss[order[j], order[k]] = max(diss(order[i], order[j]), diss(order[i], order[k]))

    return diss

