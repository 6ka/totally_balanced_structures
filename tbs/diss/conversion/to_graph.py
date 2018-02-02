from tbs.graph import Graph


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
