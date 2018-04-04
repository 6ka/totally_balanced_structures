import json

from ._mixed_graph import MixedGraph, UNDIRECTED_EDGE


class Graph(MixedGraph):
    """Generic undirected Graph class."""

    def __init__(self, vertices=tuple(), edges=tuple()):
        """An undirected graph.

        Args:
            vertices (iterable): each vertex must be *hashable*.
            edges(iterable): list of pair (x, y) where *x* and *y* are vertices. Edges whose one end is not
                a vertex are discarded.
        """
        super().__init__(vertices, undirected_edges=edges)

    @classmethod
    def from_graph(cls, graph, vertices=None):
        """Create graph from another graph.

        Args:
            graph(MixedGraph): a graph
            vertices(iterable): a subset of vertices. If not set, the whole set of vertices is considered.

        If the graph is directed or mixed, only take the undirected edges.

        Returns(Graph): A new graph.
        """

        undirected, directed = graph._edges
        if vertices is None:
            vertices = graph.vertices

        return cls(vertices, undirected)

    @classmethod
    def from_json(cls, json_graph, id_to_vertex_conversion=json.loads):
        """jsgongraph to mixed-graph


        Args:
            json_graph(dict):  https://github.com/jsongraph format.
            id_to_vertex_conversion(str->object): each id is converterted into a vertex = id_to_vertex_conversion(id).
                    By defaults, node ids are json.loads() to produce vertices. Thus if the node id is "1"
                    the associated vertex s the int 1.
        Returns(Graph): the graph associated with the json
        """

        vertices, undirected, directed = cls._graph_parts_from_json(json_graph, id_to_vertex_conversion)
        return cls(vertices, undirected)

    @classmethod
    def from_neighborhoods(cls, neighbors):
        """Create graph from a neighborhood.

        Args:
            neighbors(dict): keys are vertices and values iterable of neighbors.

        Returns(Graph):
            A new graph
        """

        return cls().update([(x, y) for x in neighbors for y in neighbors[x]])

    @classmethod
    def from_edges(cls, edges):
        """Create graph from a set of edges.

        Args:
            edges(iterable): iterable of edges.

        Returns(Graph):
            A new graph
        """

        return cls().update(edges)

    @classmethod
    def from_dissimilarity(cls, dissimilarity, threshold=None):
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

        self = cls(elems)
        for i, x in enumerate(elems):
            for y in elems[i+1:]:
                if threshold is None or dissimilarity(x, y) <= threshold:
                    self.update([(x, y)])
                    self[x, y] = dissimilarity(x, y)

        return self

    def __repr__(self):
        undirected, directed = self._edges
        return "".join(["Graph(",
                        repr(self.vertices),
                        ", ", repr(undirected),
                        ")"])

    def update(self, edges, node_creation=True):
        """Add edges.

        Each edge in *edges* is added if not already present.

        If an edge is already present but not of the same type (undirected or directed), the edge is replaced.

        Args:
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).
            node_creation(bool): If :const:`False`, edges using vertices not in the graph are discarded. If
                :const:`True`, missing vertices are added in the graph.

        Raises:
            ValueError: if kind is unknown.
        Returns:
            self (for possible chaining).
        """
        return super().update(UNDIRECTED_EDGE, edges, node_creation=node_creation)

    @property
    def edges(self):
        """All (directed) edges.

        returns(frozenset):
            A :class:`frozenset` of of 2-element tuples (the directed edges).
        """

        return self._edges[0]

    def __call__(self, x, closed=False):
        """Neighborhood of vertex x.

        Args:
            x: a vertex.
            closed(bool): if true adds *x* in the returns (closed neighborhood).

        Raises:
            ValueError: if *x* is not a vertex.

        Returns(frozenset):
            the neighbors of *x* according to the boolean specifications.

        """
        return super().__call__(x, undirected=True, closed=closed)

    def isa_edge(self, x, y):
        """test if (x, y) is an edge.

        Args:
            x: a vertex.
            y: a vertex.


        Returns(bool):
            By default, returns True if (x, y) is an edge, False otherwise.
        """

        return super().isa_edge(x, y, UNDIRECTED_EDGE)
