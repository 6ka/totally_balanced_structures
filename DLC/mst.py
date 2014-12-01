# -*- coding: utf-8 -*-

from DLC.graph import Graph
import sys

def mst_from_graph(graph, f=lambda x: x, root=None):
    """Minimal spanning tree (according to f).

    :param graph: graph
    :type graph: :class:`CTK.graph.Graph`
    :param root: A vertex. If :const:`None` a vertex to begin with
                 is chosen.
    :param f: function taking the attribute of an edge as argument and
              returns a real number.
    :type f: ``function``

    :raise: :exc:`ValueError` if *graph* is not connected.
    """

    if root is None:
        for root in graph:
            break

    reminding_vertices = list(graph)
    prim_tree = graph.__class__((root,))
    reminding_vertices.remove(root)
    pivot = root

    d = {}
    proche = {}
    for i in range(len(graph)-1):
        for z in graph[pivot]:
            if z in prim_tree:
                continue
            if (z not in d) or (f(graph(pivot, z)) < d[z]):
                proche[z] = pivot
                d[z] = f(graph(pivot, z))

        pivot = None
        for x in reminding_vertices:
            if pivot is None or (pivot not in d):
                pivot = x
            elif x in d and d[x] < d[pivot]:
                pivot = x

        if pivot not in d:
            raise ValueError("not connected graph")

        prim_tree.add(pivot)
        reminding_vertices.remove(pivot)
        prim_tree.update(((pivot, proche[pivot], graph(pivot, proche[pivot])),))

    return prim_tree


def mst_from_dissimilarity(dissimilarity, root=None, elements=None):
    """Minimal spanning tree (according to f).

    :param root: A vertex. If :const:`None` a vertex to begin with
                 is chosen.
    :param dissimilarity: dissimilarity whose values are comparable
    :type dissimilarity: :class:`CTK.diss.Diss`

    :raise: :exc:`ValueError` if *graph* is not connected.
    """
    if elements is None:
        elements = list(dissimilarity)
    if root is None:
        for root in dissimilarity:
            break

    reminding_vertices = list(elements)
    prim_tree = Graph((root,))
    reminding_vertices.remove(root)
    pivot = root

    d = {}
    proche = {}
    for i in range(len(elements)-1):
        print(i, len(elements) - 1, file=sys.stderr)
        for z in elements:
            if z in prim_tree:
                continue
            if (z not in d) or (dissimilarity(pivot, z) < d[z]):
                proche[z] = pivot
                d[z] = dissimilarity(pivot, z)

        pivot = None
        for x in reminding_vertices:
            if pivot is None or (pivot not in d):
                pivot = x
            elif x in d and d[x] < d[pivot]:
                pivot = x

        if pivot not in d:
            raise ValueError("not connected graph")

        prim_tree.add(pivot)
        reminding_vertices.remove(pivot)
        prim_tree.update(((pivot, proche[pivot], dissimilarity(pivot, proche[pivot])),))

    return prim_tree
