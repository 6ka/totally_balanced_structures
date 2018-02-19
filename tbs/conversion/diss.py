"""Convert :class:`tbs.diss.Diss` to various types.

.. currentmodule:: tbs.conversion.diss

Module content
--------------

"""

__author__ = 'francois'
__all__ = ["to_graph", "to_string"]


from ..graph import Graph


def to_graph(dissimilarity, threshold=None):
    """Threshold graph of *dissimilarity* at height *threshold*.

    :param dissimilarity: to be converted in graph.
    :type dissimilarity: :class:`diss.Diss`

    :param threshold: If :const:`None`, the maximal value of *dissimilarity* is used.
    :type threshold: must be `comparable` with *dissimilarity*'s values

    :return: a graph with vertex set equal to the elements of *dissimilarity* and *xy*
             is an edge iff *dissimilarity*\ (x, y) <= *threshold*.
    :rtype: :class:`Graph`
    """

    elems = list(dissimilarity)
    edges = []

    for i, x in enumerate(elems):
        for y in elems[i+1:]:
            if threshold is None or dissimilarity(x, y) <= threshold:
                edges.append((x, y, dissimilarity(x, y)))

    return Graph(elems).update(edges)


def to_string(dissimilarity, kind="square", sep=" ", alias=None):
    """Dissimilarity String representation.

    :param dissimilarity: dissimilarity to convert
    :type dissimilarity: :class:`tbs.diss.Diss`
    :param kind: ``'square'``, ``'squarel'``, ``'upper'``, ``'upperl'``,
                 ``'lower'``, ``'lowerl'``, ``'squarep'``, ``'upperp'`` or ``'lowerp'``.
    :param sep: delimiter string.
    :type sep: :class:`str`
    :type alias: :class:`dict` whose keys are the dissimilarity elements and values
                 the associated aliases. If :const:`None` no conversions.

    :rtype: :class:`str`
    """

    elems = list(dissimilarity)
    elems_alias = list(dissimilarity)

    if alias:
        for i in range(len(elems)):
            elems_alias[i] = alias[elems[i]]

    aff = ""

    if kind.endswith(('l', 'p')):
        max_label = max([len(str(x)) for x in elems_alias])
    else:
        max_label = 0

    my_max = max([len(str(x)) for x in dissimilarity.values(True)])

    if kind.endswith('p'):
        aff += str(len(elems))+"\n"
    for x in range(len(elems)):
        if kind.endswith('l') or kind.endswith('p'):
            if sep.strip():
                aff += str(elems_alias[x])
            else:
                aff += str(elems_alias[x]).ljust(max_label)
            if kind.endswith('l') or kind.startswith("square") or \
                    (x < len(elems) - 1 and kind.startswith("upper")) or (x != 0 and kind.startswith("lower")):
                aff += sep
        for y in range(len(elems)):
            if y < x:
                if (kind.endswith(('l', 'p')) and not kind.startswith("upper")) or \
                        (not kind.endswith(('l', 'p')) and kind != "upper"):
                    aff += str(dissimilarity(elems[x], elems[y])).rjust(my_max) + sep
                elif kind.startswith("upper") and not (kind.endswith("p") and x == len(elems) - 1):
                    aff += str().rjust(my_max) + sep
            elif x == y:
                if kind == "upperp":
                    if y < len(elems) - 1:
                        aff += str().rjust(my_max) + sep
                elif kind == "lowerp":
                    pass
                else:
                    aff += str(dissimilarity(elems[x], elems[y])).rjust(my_max) + sep
            elif (kind.endswith(('l', 'p')) and not kind.startswith("lower")) or \
                    (not kind.endswith(('l', 'p')) and kind != "lower"):
                aff += str(dissimilarity(elems[x], elems[y])).rjust(my_max)
                aff += sep
        if aff.endswith(sep):
            # trailing sep
            aff = aff[:-len(sep)]
        if x < len(elems) - 1:
            aff += "\n"

    return aff