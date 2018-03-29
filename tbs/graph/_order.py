import collections

from ._directed_graph import DirectedGraph
from ._mixed_graph import MixedGraph


def dfs(graph, key=None):
    """depth first search.

    Args:
        graph(MixedGraph): a mixed graph
        key(x->order position): Used for sorting the examination order (equivalent to sort with parameter key=key)

    Returns(list): dfs order.
    """
    dfs_order = []

    is_seen = set()
    stack = []

    elements = list(graph)
    if key:
        elements.sort(key=key)

    for x in elements:
        stack.append(x)
        while stack:
            v = stack.pop()
            if v not in is_seen:
                is_seen.add(v)
                dfs_order.append(v)
                neighbors = list(graph(v))
                if key:
                    neighbors.sort(key=key)
                stack.extend(neighbors)

    return dfs_order


def dfs_from_vertex(graph, vertex):
    """depth first search from a chosen vertex.

    Args:
        graph(MixedGraph): a mixed graph
        vertex: the vertex from which to begin the search

    Returns(list): dfs order.
    """
    return dfs(graph, key=lambda x: x == vertex and 1 or 2)


def bfs(graph, key=None):
    """breadth first search.

    Args:
        graph(MixedGraph): a mixed graph
        key(x->order position): Used for sorting the examination order (equivalent to sort with parameter key=key)

    Returns(list): dfs order.
    """


    bfs_order = []

    is_seen = set()

    fifo = collections.deque()

    elements = list(graph)
    if key:
        elements.sort(key=key)

    for x in elements:
        if x not in is_seen:
            is_seen.add(x)
            fifo.appendleft(x)
        while fifo:
            v = fifo.pop()
            bfs_order.append(v)
            neighbors = list(graph(v))
            if key:
                neighbors.sort(key=key)

            for w in neighbors:
                if w not in is_seen:
                    is_seen.add(w)
                    fifo.appendleft(w)

    return bfs_order


def bfs_from_vertex(graph, vertex):
    """breadth first search from a chosen vertex.

   Args:
       graph(MixedGraph): a mixed graph
       vertex: the vertex from which to begin the search

   Returns(list): bfs order.
   """

    return bfs(graph, key=lambda x: x == vertex and 1 or 2)


def topological_sort(dag, key=None):
    """Topologigical sort.

    Args:
        dag(DirectedGraph): a directed acyclic graph
        key(x->order position): Used for sorting the examination order (equivalent to sort with parameter key=key)

    Raises(TypeError): if *dag* is not acyclic.

    Returns(list): topological order.
    """

    reverse_order = []
    is_seen = set()
    is_seen_local = set()

    def visit(vertex):
        if vertex in is_seen:
            return
        elif vertex in is_seen_local:
            raise TypeError

        is_seen_local.add(vertex)

        visit_list = list(dag(vertex))
        if key is not None:
            visit_list.sort(key=key)
            visit_list.reverse()
        for neighbor in visit_list:
            visit(neighbor)

        is_seen.add(vertex)
        is_seen_local.remove(vertex)
        reverse_order.append(vertex)

    elements = list(dag)
    if key:
        elements.sort(key=key)
        elements.reverse()

    for x in elements:
        visit(x)

    reverse_order.reverse()
    return reverse_order


def direct_acyclic_graph_to_direct_comparability_graph(dag):
    """ Comparability graph from a dag.

    Args:
        dag(DirectedGraph): a directed acyclic graph

    Returns(DirectedGraph):
        The direct comparability graph of *dag* with no loop (to preserve acyclicity).
    """
    direct_comparability = DirectedGraph(vertices=dag.vertices)

    for vertex in topological_sort(dag):
        for cover in dag(vertex, begin=False, end=True):
            direct_comparability.update([(cover, vertex)])
            direct_comparability.update([(y, vertex) for y in direct_comparability(cover, begin=False, end=True)])

    return direct_comparability


def direct_comparability_graph_to_hase_diagram(direct_comparability):
    """ hase diagram from a directed comparability graph.

    Args:
        direct_comparability(DirectedGraph): a directed comparability graph.

    No check whether dag is a comparability graph or not.

    Returns(DirectedGraph):
        The direct comparability graph of *dag*
    """

    hase_diagram = DirectedGraph.from_graph(direct_comparability)

    hase_diagram.difference(((x, x) for x in direct_comparability))

    for x, y in direct_comparability.edges:
        if direct_comparability(x).intersection(direct_comparability(y, begin=False, end=True)):
            hase_diagram.difference([(x, y)])
            continue
    return hase_diagram
