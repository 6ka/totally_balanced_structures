# -*- coding: utf-8 -*-
from graph import Graph


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