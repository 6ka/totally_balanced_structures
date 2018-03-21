from ..diss import Diss
from ._order_finder import order_by_map, order_by_map_partition


def isa_chordal_order(diss, possible_order):
    """ Check if a *possible_order* is an elimination one for a given *diss*.

    Args:
        diss(Diss): a dissimilarity
        possible_order(list): vertices order

    Returns:
        :class:`bool`

    """

    if set(possible_order) != set(diss):
        return False

    for i in range(len(possible_order)):
        for j in range(i, len(possible_order)):
            for k in range(j, len(possible_order)):
                if diss(possible_order[j], possible_order[k]) > max(diss(possible_order[i], possible_order[j]),
                                                                    diss(possible_order[i], possible_order[k])):
                    return False

    return True


def chordal_order(diss):
    """ Return a good chordal order.

    If the dissimilarity is not chordal, returns a good approximation.

    Args:
        diss(Diss):

    Returns:
        A vertex ordering in a `list`

    """

    return order_by_map(diss, lambda x, y, z: diss(y, z) > max(diss(x, y), diss(x, z)) and 1 or 0)


def chordal_order_partition(diss):
    """ Return a good chordal order.

    If the dissimilarity is not chordal, returns a good approximation.

    Args:
        diss(Diss):

    Returns:
        A vertex ordering in a `list`

    """

    return order_by_map_partition(diss, lambda x, y, z: diss(y, z) > max(diss(x, y), diss(x, z)) and 1 or 0)
