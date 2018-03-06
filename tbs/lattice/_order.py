__author__ = 'cchatel', 'fbrucker'

__all__ = ["isa_lattice_directed_comparability_graph"]

from ..graph import topological_sort


def isa_lattice_directed_comparability_graph(dag):
    """True if *dag* is the directed comparability graph of a lattice order.

    Args:
        dag(DirectedGraph): possible lattice directed comparability graph

    returns(bool):
        True if graph is the directed comparability graph of a lattice order, False otherwise.
    """

    if not dag:
        return True

    # no cycle
    try:
        topological_order = topological_sort(dag)
    except TypeError:
        return False

    # minium and maximum
    if len(dag(topological_order[0], begin=False, end=True)) > 0:
        return False
    if len(dag(topological_order[-1], begin=True, end=False)) > 0:
        return False
    for x in topological_order[1:-1]:
        if not dag(x, begin=False, end=True) or not dag(x, begin=True, end=False):
            return False


    # sup / inf
    for i in range(len(topological_order)):
        for j in range(i + 1, len(topological_order)):
            x = topological_order[i]
            y = topological_order[j]

            sup = None
            others = []
            for z in dag(x, closed=True):
                if y == z or dag.isa_edge(y, z):
                    if sup is None or dag.isa_edge(z, sup):
                        sup = z
                    elif not dag.isa_edge(sup, z):
                        others.append(z)
            for z in others:
                if not dag.isa_edge(sup, z):
                    return False

            inf = None
            others = []
            for z in dag(x, begin=False, end=True, closed=True):
                if z == y or dag.isa_edge(z, y):
                    if inf is None or dag.isa_edge(inf, z):
                        inf = z
                    elif not dag.isa_edge(z, inf):
                        others.append(z)
            for z in others:
                if not dag.isa_edge(z, inf):
                    return False

    return True
