class CircuitError(Exception):
    """Absorbent circuit."""

    def __init__(self, value):
        self.value = value


def path(graph, x, y, f=lambda x: 1, forbidden_vertices=frozenset()):
    """A minimal path (according to f) from *x* to *y*.

    :param forbidden_vertices: set of vertices which are not in the path
    :param x: a vertex.
    :param y: a vertex.

    :param f: function taking the attribute of an edge as argument and
             returns a real number.
    :type f: ``function``

    :raises: :exc:`ValueError` if either *x* or *y* is not a vertex.

    :return: a path from *x* to *y* or an empty list if *x* and *y* are
             not connected.
    :rtype: :class:`list`
    """

    if x not in graph._neighborhood or y not in graph._neighborhood:
        raise ValueError("Not a vertex")

    if x == y:
        return [x]

    father, dist = paths_from(graph, x, f, forbidden_vertices)

    if y not in father:
        return []
    the_path = [y]
    z = father[y]
    while z != x:
        the_path.append(z)
        z = father[z]

    the_path.append(x)
    the_path.reverse()

    return the_path


def paths_from(graph, root, f=lambda x: 1, forbidden_vertices=frozenset()):
    """Shortest paths (Bellman-Ford algorithm).

    Find a shortest path (according to f) between vertex *root*
    and all the other vertices (if a path exists).

    :param forbidden_vertices: set of vertices which are not in the path
    :param root: a vertex.

    :param f: function taking the attribute of an edge as argument and
             returns a real number.
    :type f: ``function``

    :raise: :exc:`CircuitError` if an absorbent circuit exists.

    :return: a couple of maps (predecessor_in_path, distance_from_root).
    :rtype: a typle of two :class:`dict`
    """

    return _inner_path_tree(graph, root, f, forbidden_vertices)


def _inner_path_tree(graph, root, f=lambda x: 1, forbidden_vertices=frozenset(), stop_if_vertex=None):
    """Shortest paths (Bellman-Ford algorithm).

    Find a shortest path (according to f) between vertex *root*
    and all the other vertices (if a path exists).

    :param root: a vertex.
    :param stop_if_vertex: algorithm stops after reaching this vertex. Uses for finding an unique path.

    :param forbidden_vertices: set of vertices which are not in the path

    :param f: function taking the attribute of an edge as argument and
             returns a real number.
    :type f: ``function``

    :raise: :exc:`CircuitError` if an absorbent circuit exists.

    :return: a couple of maps (predecessor_in_path, distance_from_root).
    :rtype: a typle of two :class:`dict`
    """

    k = 0
    n = len(graph)

    father = {root: root}
    dist = {root: 0}
    change = True

    while k < n and change:
        change = False
        k += 1
        for x in graph:
            for y in graph[x]:
                if y in forbidden_vertices:
                    continue
                if x in dist and (y not in dist or dist[y] > dist[x] + f(graph(x, y))):
                    dist[y] = dist[x] + f(graph(x, y))
                    father[y] = x
                    if y == stop_if_vertex:
                        return father, dist
                    change = True

    if change:
        raise CircuitError("")
    return father, dist


def connected_parts(graph, vertex_subset=None):
    """Partition the vertex according to its connected parts.

    :param vertex_subset: set of vertices. If ``None``, the whole vertex set
              is considered.
    :type vertex_subset: iterable

    :return: a partition.
    :rtype: :class:`frozenset`
    """

    if vertex_subset is None:
        vertex_subset = list(graph)

    classe = {}
    for x in vertex_subset:
        classe[x] = x
    for e in graph.edges():
        x, y = e
        if x not in vertex_subset or y not in vertex_subset:
            continue

        if classe[x] != classe[y]:
            xx = classe[x]
            yy = classe[y]
            for u in classe:
                if classe[u] == yy:
                    classe[u] = xx
    p = set()

    for x in vertex_subset:
        if classe[x] == x:
            elems = frozenset([y for y in vertex_subset if classe[y] == x])
            p.add(elems)
    return frozenset(p)

