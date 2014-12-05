# -*- coding: utf-8 -*-

from DLC.graph import Graph

import DLC


def subdominant_number_step(number_elements):
    n2 = number_elements * (number_elements - 1) / 2
    copy_diss = n2
    add_edges = n2
    find_path = n2
    update_quartet = n2
    find_min = n2
    number_step = n2
    return copy_diss + add_edges + number_step * (find_min + find_path + update_quartet)


def subdominant(diss):
    """Subbominant chordal quasi-ultrametric :cite:`brucker-gely2009`.

    :param diss: real dissimilarity
    :type diss: CTK.diss.Diss :class:`CTK.diss.Diss`

    :rtype: :class:`CTK.diss.Diss`
    """

    def ordering_quartet(vertex_x, vertex_y):
        for elem in q:
            if elem in (vertex_x, vertex_y):
                continue
            for t in q:
                if t in (vertex_x, vertex_y, elem):
                    continue
                howmuch = 0
                u, v = None, None
                if (vertex_x, elem) in examined_edges or (elem, vertex_x) in examined_edges:
                    howmuch += 1
                else:
                    u, v = vertex_x, elem
                if (vertex_x, t) in examined_edges or (t, vertex_x) in examined_edges:
                    howmuch += 1
                else:
                    u, v = vertex_x, t
                if (vertex_y, elem) in examined_edges or (elem, vertex_y) in examined_edges:
                    howmuch += 1
                else:
                    u, v = vertex_y, elem
                if (vertex_y, t) in examined_edges or (t, vertex_y) in examined_edges:
                    howmuch += 1
                else:
                    u, v = vertex_y, t
                if (elem, t) in examined_edges or (t, elem) in examined_edges:
                    howmuch += 1
                else:
                    u, v = elem, t
                if howmuch == 4:
                    quartet = [vertex_x, vertex_y, elem, t]
                    quartet.remove(u)
                    quartet.remove(v)
                    a, b = quartet.pop(), quartet.pop()

                    if not (not (q(a, b) >= max(q(a, u), q(b, u)) and
                                 q(u, v) > max(q(a, b), q(a, v), q(b, v))) and not (q(a, b) >= max(q(a, v), q(b, v)) and
                                                                                    q(u, v) > max(q(a, b), q(a, u),
                                                                                    q(b, u)))):
                        q[u, v] = q(vertex_x, vertex_y)

    def min_edges():
        minuv = None
        for edge in remaining_edges:
            edge_x, edge_y = edge
            if minuv is None:
                minuv = edge
            else:
                u, v = minuv
                if q(edge_x, edge_y) < q(u, v):
                    minuv = edge
        return minuv

    n2 = len(diss) * (len(diss) - 1) / 2
    q = diss.copy()
    DLC.progress_status.add(n2)
    elems = list(q)
    threshold_graph = Graph(diss)
    remaining_edges = set()
    for i, x in enumerate(elems):
        for y in elems[i + 1:]:
            if x != y:
                remaining_edges.add((x, y))

    DLC.progress_status.add(n2)
    examined_edges = set()
    while remaining_edges:
        xy = min_edges()
        remaining_edges.remove(xy)
        x, y = xy
        DLC.progress_status.add(n2)
        path = threshold_graph.a_path(x, y,
                                      forbidden_vertices=set(threshold_graph[y]).intersection(set(threshold_graph[x])))
        DLC.progress_status.add(n2)
        threshold_graph.update([(x, y)])

        for z in path:
            if z in (x, y):
                continue
            if (x, z) not in examined_edges and (z, x) not in examined_edges:
                q[x, z] = q[x, y]
            if (y, z) not in examined_edges and (z, y) not in examined_edges:
                q[y, z] = q[x, y]
        ordering_quartet(x, y)
        examined_edges.add(xy)
        DLC.progress_status.add(n2)

    return q