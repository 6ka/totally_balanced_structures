from ._directed_graph import DirectedGraph


def dfs(graph, start_vertex, visit, order_key=None):
    """depth first search.

    If the graph is not connected or directed, may not cover all the vertices.

    :param start_vertex: starting vertex
    :param visit: visit done for each new seen vertex.
    :type visit: `function` taking a vertex as parameter.

    :param order_key: order for neighbor travel. sort with key=order
    :type order_key: function
    """
    is_seen = set()

    def rec_dfs(vertex):
        visit(vertex)
        is_seen.add(vertex)
        visit_list = graph[vertex]
        if order_key is not None:
            visit_list.sort(key=order_key)
        for neighbor in visit_list:
            if neighbor not in is_seen:
                rec_dfs(neighbor)

    rec_dfs(start_vertex)


def bfs(graph, start_vertex, visit, order_key=None):
    """breath first search.

    If the graph is not connected or directed, may not cover all the vertices.

    :param order_key: order for which the vertices are taken
    :param start_vertex: starting vertex
    :param visit: visit done for each new seen vertex.
    :type visit: `function` taking a vertex as parameter.

    """
    import collections

    fifo = collections.deque((start_vertex,))
    is_seen = {start_vertex}

    while fifo:
        vertex = fifo.pop()
        visit(vertex)
        visit_list = graph[vertex]
        if order_key is not None:
            visit_list.sort(key=order_key)
        for neighbor in visit_list:
            if neighbor not in is_seen:
                is_seen.add(neighbor)
                fifo.appendleft(neighbor)


def topological_sort(dag, start_vertex=None, order_key=None):
    """Topologigical sort.

    If the graph is not connected or directed, may not cover all the vertices.

    Args:
        dag(DirectedGraph): a directed acyclic graph

    :param order_key: order for neighbor travel. sort with key=order
    :type order_key: function

    :rtype: :class:`iterator` on vertex
    """

    reverse_order = []
    is_seen = set()

    def rec_sort(vertex):
        is_seen.add(vertex)
        visit_list = dag[vertex]
        if order_key is not None:
            visit_list.sort(key=order_key)
        for neighbor in visit_list:
            if neighbor not in is_seen:
                rec_sort(neighbor)

        reverse_order.append(vertex)

    if start_vertex is None:
        elements = list(dag)
        if order_key:
            elements.sort(key=order_key)

        start_vertex = elements[0]
        for start_vertex in elements:
            if not dag(start_vertex, begin=False, end=True):
                break

    rec_sort(start_vertex)
    return reversed(reverse_order)


def _topological_sort(dag, order_key=None):
    """Topologigical sort.

    If the graph is not connected or directed, may not cover all the vertices.

    Args:
        dag(DirectedGraph): a directed acyclic graph
        order_key(x->order position): Used for sorting the examination order (sort with key=order)

    Raises(TypeError): if *dag* is not acyclic.

    Returns(iterator): topological order.
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
        if order_key is not None:
            visit_list.sort(key=order_key)
        for neighbor in visit_list:
            visit(neighbor)

        is_seen.add(vertex)
        is_seen_local.remove(vertex)
        reverse_order.append(vertex)

    elements = list(dag)
    if order_key:
        elements.sort(key=order_key)

    for x in elements:
        visit(x)

    return reversed(reverse_order)


def direct_acyclic_graph_to_direct_comparability_graph(dag):
    """ Comparability graph from a dag.

    Args:
        dag(DirectedGraph): a directed acyclic graph

    Returns(DirectedGraph):
        The direct comparability graph of *dag*
    """
    direct_comparability = DirectedGraph(vertices=dag.vertices)

    for vertex in _topological_sort(dag):
        for cover in dag(vertex, begin=False, end=True):
            direct_comparability.update([(cover, vertex)])
            direct_comparability.update([(y, vertex) for y in direct_comparability(cover, begin=False, end=True)])

    return direct_comparability


def direct_acyclic_graph_to_hase_diagram(dag):
    """ hase diagram from a dag.

    Args:
        dag(DirectedGraph): a directed acyclic graph

    Returns(DirectedGraph):
        The direct comparability graph of *dag*
    """

    direct_comparability = DirectedGraph.from_graph(dag)

    direct_comparability.difference(((x, x) for x in direct_comparability))

    for x, y in direct_acyclic_graph_to_direct_comparability_graph(dag).edges:
        if direct_comparability(x).intersection(direct_comparability(y, begin=False, end=True)):
            direct_comparability.difference([(x, y)])
            continue
    return direct_comparability

