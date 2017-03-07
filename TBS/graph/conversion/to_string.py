# -*- coding: utf-8 -*-

"""Conversion to :class:`str`.
"""

__author__ = 'fbrucker'


def to_string(graph, kind="edges", sep=' '):
    """Graph string representation.

    :param graph: graph to convert
    :type graph: TBS.graph.Graph :class:`TBS.graph.Graph`
    :param kind: ``'graph'``, ``'edges'``, ``'edgesNb'``, ``'dotBasic'``.
    :param sep: delimiter string. Only used for ``'edges'`` and ``'edgesNb'`` representation.
    :type sep: one character

    :rtype: :class:`str`
    """

    if kind == "graph":
        vertex_set = "{"
        for x in graph:
            vertex_set += str(x) + ", "
        if len(vertex_set) > 1:
            #delete trailing coma
            vertex_set = vertex_set[:-2]
        vertex_set += "}"
        edge_set = "{"
        if graph.directed:
            begin = '('
            end = ')'
        else:
            begin = '{'
            end = '}'

        for x, y in graph.edges():
            edge_set += begin + str(x) + ', ' + str(y) + end + ', '
        if len(edge_set) > 1:
            #trailing comma
            edge_set = edge_set[:-2]
        edge_set += "}"
        return "(" + vertex_set + ", " + edge_set + ")"
    elif kind == "dotBasic":
        if graph.directed:
            s = "digraph {\n"
        else:
            s = "strict graph {\n"
        for x, y in graph.edges():
            if graph.directed:
                edge = "\"" + str(x) + "\"" + " -> " + "\"" + str(y) + "\"" + "\n"
            else:
                edge = "\"" + str(x) + "\"" + " -- " + "\"" + str(y) + "\"" + "\n"
            s += edge

        for x in graph:
            has_neigbors = (graph.degree(x) > 0)
            if not has_neigbors and graph.directed:
                for y in graph:
                    if x == y:
                        continue
                    if graph.isa_edge(y, x):
                        has_neigbors = True
                        break
            if not has_neigbors:
                s += "\"" + str(x) + "\"" + "\n"
        return s + "}"
    else:
        #edges or edgesNb
        if kind == "edgesNb":
            s = str(len(graph.edges())) + "\n"
        else:
            s = ""
        max_label = max([len(str(x)) for x in graph])
        for x, y, z in graph.edges(True):
            s += str(x).ljust(max_label) + sep + str(y).ljust(max_label)
            if z is not None:
                s += sep + str(z)
            s += "\n"
        for x in graph:
            has_neigbors = (graph.degree(x) > 0)
            if not has_neigbors and graph.directed:
                for y in graph:
                    if x == y:
                        continue
                    if graph.isa_edge(y, x):
                        has_neigbors = True
                        break
            if not has_neigbors:
                s += str(x) + "\n"
        #trailing '\n'
        return s[:-1]