# -*- coding: utf-8 -*-
from ._graph import Graph


def mst_from_set(elements, f=lambda x, y: 1, root=None):
    """Minimal spanning tree (according to f).
    """

    mst = Graph(elements)

    if root is None:
        for root in elements:
            break

    reminding_vertices = set(elements)
    reminding_vertices.remove(root)
    pivot = root

    d = {}
    neighbor = {}
    for i in range(len(elements)-1):
        for z in reminding_vertices:
            if (z not in d) or (f(pivot, z) < d[z]):
                neighbor[z] = pivot
                d[z] = f(pivot, z)

        pivot = None
        for x in reminding_vertices:
            if pivot is None or (pivot not in d):
                pivot = x
            elif x in d and d[x] < d[pivot]:
                pivot = x

        reminding_vertices.remove(pivot)
        mst.update([(pivot, neighbor[pivot])])

    return mst


def connected_parts(graph, vertex_subset=None):
    """Partition the vertex according to its connected parts.

    Args:
        graph(Graph): undirected graph
        vertex_subset(iterable): set of vertices. If ``None``, the whole vertex set
              is considered.

        returns(frozenset): a frozenset of frosenset of connected parts.
    """

    if vertex_subset is None:
        vertex_subset = list(graph)

    connected_part = dict()
    for x in vertex_subset:
        connected_part[x] = x
    for x, y in graph.edges:
        if x not in vertex_subset or y not in vertex_subset:
            continue

        if connected_part[x] != connected_part[y]:
            xx = connected_part[x]
            yy = connected_part[y]
            for u in connected_part:
                if connected_part[u] == yy:
                    connected_part[u] = xx
    p = set()

    for x in vertex_subset:
        if connected_part[x] == x:
            elems = frozenset([y for y in vertex_subset if connected_part[y] == x])
            p.add(elems)
    return frozenset(p)
