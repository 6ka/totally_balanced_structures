# -*- coding: utf-8 -*-

import sys
import datetime
from DLC.graph import Graph


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

                    if not (not (q.get_by_pos(a, b) >= max(q.get_by_pos(a, u), q.get_by_pos(b, u)) and
                                         q.get_by_pos(u, v) > max(q.get_by_pos(a, b), q.get_by_pos(a, v),
                                                                  q.get_by_pos(b, v))) and not (
                                    q.get_by_pos(a, b) >= max(q.get_by_pos(a, v), q.get_by_pos(b, v)) and
                                    q.get_by_pos(u, v) > max(q.get_by_pos(a, b), q.get_by_pos(a, u),
                                                             q.get_by_pos(b, u)))):
                        q.set_by_pos(u, v, q.get_by_pos(vertex_x, vertex_y))

    def min_edges():
        minuv = None
        for edge in remaining_edges:
            edge_x, edge_y = edge
            if minuv is None:
                minuv = edge
            else:
                u, v = minuv
                if q.get_by_pos(edge_x, edge_y) < q.get_by_pos(u, v):
                    minuv = edge
        return minuv

    q = diss.copy()
    elems = list(range(len(q)))
    threshold_graph = Graph(elems)
    remaining_edges = set()
    for i, x in enumerate(elems):
        for y in elems[i + 1:]:
            if x != y:
                remaining_edges.add((x, y))
    examined_edges = set()
    total_number = len(remaining_edges)
    percent = 1
    while remaining_edges:
        # if len(remaining_edges) / total_number < percent:
        #     print("{0:2.0f}%".format(100 * (1 - len(remaining_edges) / total_number)), datetime.datetime.now(), file=sys.stderr)
        #     percent -= .01
        xy = min_edges()
        remaining_edges.remove(xy)
        x, y = xy

        path = threshold_graph.path(x, y,
                                      forbidden_vertices=set(threshold_graph[y]).intersection(set(threshold_graph[x])))
        threshold_graph.update([(x, y)])
        for z in path:
            if z in (x, y):
                continue
            if (x, z) not in examined_edges and (z, x) not in examined_edges:
                q.set_by_pos(x, z, q.get_by_pos(x, y))
            if (y, z) not in examined_edges and (z, y) not in examined_edges:
                q.set_by_pos(y, z, q.get_by_pos(x, y))
        ordering_quartet(x, y)
        examined_edges.add(xy)

    return q