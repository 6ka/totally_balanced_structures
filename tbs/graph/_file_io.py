"""Load and save :class:`tbs.graph.Graph`

.. currentmodule:: tbs.graph.file_io

Module content
--------------

"""

from ..conversion.graph import to_string
from ._graph import Graph


__author__ = 'fbrucker'
__all__ = ["load", "save"]


def load(f, kind="edges", sep=None, number=True):
    """Load a graph from file *f*.

    Empty lines, lines containing only whitespaces and lines beginning with
     ``'#'`` are discarded.

    :param f: file
    :type f: :class:`file`
    :param kind: ``'edges'``, ``'edgesNb'``, ``'dotBasic'``.
    :param sep: delimiter string. Not used for ``'dotBasic'``.
    :type sep: :class:`str`

    :param number: if :const:`True` , values are converted into
                   :class:`float`, :class:`str` otherwise.

    :rtype: :class:`Graph`

    .. seealso:: :func:`tbs.conversion.to_string.from_graph`

    """
    lines = []
    for line in f:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    if len(lines) < 1:
        raise ValueError("file contains no usefull lines or empty file")

    loaded_graph = Graph()

    if kind == "dotBasic" and lines[0].startswith("digraph"):
        loaded_graph.directed = True
    if kind in ("edgesNb", "dotBasic"):
        lines.pop(0)
    if kind == "dotBasic":
        #last "}"
        lines.pop()

    for line in lines:
        if kind == "dotBasic" and line[-1] == ";":
            line = line[:-1]
        if kind.startswith("edges"):
            line = line.split(sep)
        elif loaded_graph.directed:
            line = line.split("->")
        else:
            line = line.split("--")

        if len(line) > 3:
            raise ValueError("line contains more than 3 fields")

        if len(line) == 1:
            #isolated vertex
            x = line[0].strip()
            if kind == "dotBasic" and x.startswith("\"") and x.endswith("\""):
                x = x[1:-1]
            if not loaded_graph.isa_vertex(x):
                loaded_graph.add(x)
            continue
        x, y = line[0].strip(), line[1].strip()
        if kind == "dotBasic" and x.startswith("\"") and x.endswith("\""):
            x = x[1:-1]
        if kind == "dotBasic" and y.startswith("\"") and y.endswith("\""):
            y = y[1:-1]
        if len(line) == 2:
            if not loaded_graph.isa_edge(x, y):
                loaded_graph.update([(x, y)])
        else:
            if not loaded_graph.isa_edge(x, y):
                if number:
                    loaded_graph.update([(x, y, float(line[2].strip()))])
                else:
                    loaded_graph.update([(x, y, line[2].strip())])
    return loaded_graph


def save(graph, f, kind="edges", sep=" "):
    """Write the dissimilarity *d* in file f

    :param graph: graph to save
    :type graph: :class:`tbs.graph.Graph`
    :param f: file
    :param kind: ``'edges'``, ``'edgesNb'``, ``'dotBasic'``.
    :param sep: delimiter string. Not used for ``'dotBasic'``.
    :type sep: :class:`str`

    .. seealso:: :func:`tbs.conversion.to_string.from_graph`
    """

    f.write(to_string(graph, kind, sep))
    return f
