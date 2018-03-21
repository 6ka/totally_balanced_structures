
from ..graph import Graph

from ._order_finder import order_by_map
from ..contextmatrix import ContextMatrix

__all__ = ["elimination_order", "isa_elimination_order",
           "simple_elimination_order",
           "strong_elimination_order"]


def isa_ultrametric_edge(graph, x, y, z):
    return not (not graph.isa_edge(y, z) and graph.isa_edge(x, y) and graph.isa_edge(x, z))


def elimination_order(graph):
    """ Return an elimination order for a chordal graph.
    
    If the graph is not chordal, returns a good approximation.
    
    Args:
        graph(Graph): a non directed graph
    
    Returns(list):
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
    """simple elimination ordering.

     Args:
        graph(Graph): a strongly chordal graph

    Returns(list):
        A simple elimination order
    """

    order = elimination_order(graph)
    cluster_matrix = [[0] * len(order) for i in range(len(order))]

    for j, x in enumerate(order):
        cluster_matrix[j][j] = 1
        for i in range(j + 1, len(order)):
            y = order[i]
            if graph.isa_edge(x, y):
                cluster_matrix[i][j] = 1

    context_matrix = ContextMatrix(cluster_matrix, order, order).reorder_doubly_lexical()

    return context_matrix.elements


def strong_elimination_order(graph):
    """Strong elimination ordering.

     Args:
        graph(Graph): a strongly chordal graph

    Returns(list):
        A strong elimination order
    """

    return simple_to_strong_elimination_order(graph, simple_elimination_order(graph))


def simple_to_strong_elimination_order(graph, simple_elimination):
    """strong elimination ordering from a simple elimination one.

    Uses the linear algorithm of "from a simple elimination ordering to a string elimination ordering in linear time"
    (sawada and Spinrad, 2003).

     Args:
        graph(Graph): a strongly chordal graph
        simple_elimination(list): simple elimination order

    Returns:
        A strong elimination order

    """

    strong_elimination_order = []
    for x in simple_to_strong_elimination_order_partition(graph, simple_elimination):
        strong_elimination_order.extend(x)

    return strong_elimination_order


def simple_to_strong_elimination_order_partition(graph, simple_elimination):
    """strong elimination ordering from a simple elimination one.

    Uses the linear algorithm of "from a simple elimination ordering to a string elimination ordering in linear time"
    (sawada and Spinrad, 2003).

     Args:
        graph(Graph): a strongly chordal graph
        simple_elimination(list): simple elimination order

    Returns:
        A strong elimination partition

    """

    strong_elimination_partition = make_sets(graph, simple_elimination)

    simple_elimination = []
    for x in strong_elimination_partition:
        simple_elimination.extend(x)

    for x in reversed(simple_elimination):
        new_list_of_sets = []
        neighborhood = set(graph(x))
        neighborhood.add(x)

        for s in strong_elimination_partition:
            if neighborhood.intersection(s) and s - neighborhood:
                new_list_of_sets.append(s - neighborhood)
                new_list_of_sets.append(neighborhood.intersection(s))
            else:
                new_list_of_sets.append(s)
        strong_elimination_partition = new_list_of_sets

    return strong_elimination_partition


def make_sets(graph, simple_elimination):
    g = Graph.from_graph(graph)

    list_of_sets = []

    for x in simple_elimination:
        if x in g:
            new_set = {x}
            new_set.update({u for u in g(x) if len(g(x)) == len(g(u))})

            list_of_sets.append(new_set)
            for u in new_set:
                g.remove(u)

    return list_of_sets
