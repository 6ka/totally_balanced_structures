

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


def topological_sort(graph, start_vertex=None, order_key=None):
    """Topologigical sort.

    If the graph is not connected or directed, may not cover all the vertices.

    Args:
        graph: a graph having only directed edges.

    :param order_key: order for neighbor travel. sort with key=order
    :type order_key: function

    :rtype: :class:`iterator` on vertex
    """

    reverse_order = []
    is_seen = set()

    def rec_sort(vertex):
        is_seen.add(vertex)
        visit_list = graph[vertex]
        if order_key is not None:
            visit_list.sort(key=order_key)
        for neighbor in visit_list:
            if neighbor not in is_seen:
                rec_sort(neighbor)

        reverse_order.append(vertex)

    if start_vertex is None:
        elements = list(graph)
        if order_key:
            elements.sort(key=order_key)

        start_vertex = elements[0]
        for start_vertex in elements:
            if not graph(start_vertex, begin=False, end=True):
                break

    rec_sort(start_vertex)
    return reversed(reverse_order)
