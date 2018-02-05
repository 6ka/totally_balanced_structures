
from ..graph import Graph
from ..diss import Diss

from .order_finder import order_by_map
from ..contextmatrix.context_matrix import ContextMatrix


def isa_ultrametric_edge(graph, x, y, z):
    return not (not graph.isa_edge(y, z) and
    graph.isa_edge(x, y) and graph.isa_edge(x, z))


def elimination_order(graph):
    """ Return an elimination order for a chordal graph.
    
    If the graph is not chordal, returns a good approximation.
    
    Args:
        graph(Graph): a non directed graph
    
    Returns:
        A vertex ordering in a `list`
    
    """

    return order_by_map(graph, lambda x, y, z: not isa_ultrametric_edge(graph, x, y, z) and 1 or 0)


def isa_elimination_order(graph, possible_order):
    """ Check if a *possible_order* is an elimination one for a given *graph*.

    Args:
        graph(Graph): a non directed graph
        possible_order(enumerable): vertices order

    Returns:
        :class:`bool`

    """

    if set(possible_order) != set(graph):
        return False

    for i in range(len(possible_order)):
        x = possible_order[i]
        for j in range(i + 1, len(possible_order)):
            y = possible_order[j]
            for k in range(j + 1, len(possible_order)):
                z = possible_order[k]
                if not isa_ultrametric_edge(graph, x, y, z):
                    return False

    return True


def simple_elimination_order(graph):

    associated_diss = Diss(graph).update(lambda x, y: graph.isa_edge(x, y) and 1 or 2)

    order = elimination_order(graph)
    cluster_matrix = [[0] * len(order) for i in range(len(order))]

    for j, x in enumerate(order):
        cluster_matrix[j][j] = 1
        for i in range(j + 1, len(order)):
            y = order[i]
            if graph.isa_edge(x, y):
                cluster_matrix[i][j] = 1

    context_matrix = ContextMatrix(cluster_matrix, order, order, copy_matrix=False).reorder_doubly_lexical_order()

    return context_matrix.elements





