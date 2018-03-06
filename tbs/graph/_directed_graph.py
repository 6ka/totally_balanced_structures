
from ._mixed_graph import MixedGraph, DIRECTED_EDGE


class DirectedGraph(MixedGraph):
    """Generic Directed Graph class."""

    def __init__(self, vertices=tuple(), edges=tuple()):
        """A mixed graph.

        Args:
            vertices (iterable): each vertex must be *hashable*.
            edges(iterable): list of pair (x, y) where *x* and *y* are vertices. Edges whose one end is not
                a vertex are discarded.
        """
        super().__init__(vertices, directed_edges=edges)

    @classmethod
    def from_graph(cls, graph, vertices=None):
        """Create graph from another graph.

        Args:
            graph: a graph
            vertices: a subset of vertices. If not set, the whole set of vertices is considered.

        Returns(DirectedGraph):
            A new graph
        """

        undirected, directed = graph._edges
        if vertices is None:
            vertices = graph.vertices

        return cls(vertices, directed)

    def __repr__(self):
        undirected, directed = self._edges
        return "".join(["DirectedGraph(",
                        repr(self.vertices),
                        ", ", repr(directed),
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
        return super().update(DIRECTED_EDGE, edges, node_creation=node_creation)

    @property
    def edges(self):
        """All (directed) edges.

        returns(frozenset):
            A :class:`frozenset` of of 2-element tuples (the directed edges).
        """

        return self._edges[1]

    def __call__(self, x, begin=True, end=False, closed=False):
        """Neighborhood of vertex x.

        Args:
            x: a vertex.
            begin(bool): if True add directed edges beginning with *x*
            end(bool): if True add directed edges ending with *x*
            closed(bool): if true adds *x* in the returns (closed neighborhood).

        Raises:
            ValueError: if *x* is not a vertex.

        Returns(frozenset):
            the neighbors of *x* according to the boolean specifications.

        """
        return super().__call__(x, undirected=False, begin=begin, end=end, closed=closed)

    def isa_edge(self, x, y):
        """test if (x, y) is an edge.

        Args:
            x: a vertex.
            y: a vertex.


        Returns(bool):
            By default, returns True if (x, y) is an edge, False otherwise.
        """

        return super().isa_edge(x, y, DIRECTED_EDGE)
