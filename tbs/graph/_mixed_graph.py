__author__ = 'fbrucker'

UNDIRECTED_EDGE = "UNDIRECTED_EDGE"
DIRECTED_EDGE = "DIRECTED_EDGE"


class MixedGraph(object):
    """Generic Mixed Graph class.
    """

    def __init__(self, vertices=tuple(), undirected_edges=tuple(), directed_edges=tuple()):
        """A mixed graph.

        Args:
            vertices (iterable): each vertex must be *hashable*.
            directed_edges(iterable): list of pair (x, y) where *x* and *y* are vertices. Edges whose one end is not
                a vertex are discarded.
            undirected_edges(iterable): same as directed_edges for undirected edges. Undirected edges replace directed
                one if they already exist.

        One Cannot have both (x, y) as undirected and directed edge.
        """

        self._vertices = frozenset()
        self._undirected = dict()  # x - y means y in dict[x] and x in dict[y]
        self._directed = dict()  # x -> y means y in dict[x]
        self._directed_dual = dict()  # x -> y means x in dict[y]

        for x in vertices:
            self.add(x)

        self.__update_directed(directed_edges, node_creation=False, delete=False)
        self.__update_undirected(undirected_edges, node_creation=False, delete=False)

    @classmethod
    def from_graph(cls, graph, vertices=None):
        """Create graph from another graph.

        Args:
            graph(MixedGraph): a graph
            vertices: a subset of vertices. If not set, the whole set of vertices is considered.

        Returns(MixedGraph):
            A new `MixedGraph`
        """

        undirected, directed = graph.edges
        if vertices is None:
            vertices = graph.vertices

        return graph.__class__(vertices, undirected, directed)

    def __repr__(self):
        undirected, directed = self.edges
        return "".join(["MixedGraph(",
                        repr(self.vertices),
                        ", ", repr(undirected),
                        ", ", repr(directed),
                        ")"])

    @property
    def vertices(self):
        """Vertex set."""

        return self._vertices

    @property
    def edges(self):
        """Undirected and directed edges.

        returns:
            A couple (U, D) where U is a :class:`frozenset` of 2-element frozenset (the undirected edges) and D is a
            frozenset of 2-element tuple (the directed edges).
        """

        return [frozenset(frozenset([x, y]) for x, Y in self._undirected.items() for y in Y),
                frozenset((x, y) for x, Y in self._directed.items() for y in Y)]

    def __nonzero__(self):
        """False if no vertex."""

        if self._vertices:
            return True
        return False

    def __eq__(self, g):
        """Same vertices, same egdes and same attribute for each edge."""

        return self.vertices == g.vertices and self.edges == g.edges

    def __ne__(self, g):
        """not ==."""

        return not self == g

    def add(self, x):
        """Add vertex *x*.

        Args:
            x(hashable): new vertex to add.
        Raises:
            ValueError: if *x* is already a vertex.
        """

        if x in self.vertices:
            raise ValueError("Already a vertex")

        self._vertices = self._vertices.union([x])
        self._undirected[x] = dict()
        self._directed[x] = dict()
        self._directed_dual[x] = dict()

    def remove(self, x):
        """Remove vertex *x*.

        Args:
            x: a vertex

        Raises:
            :exc:`ValueError` if *x* is not a vertex.
        """

        if x not in self.vertices:
            raise ValueError("Not a vertex")

        self._vertices = self._vertices.difference([x])
        for y in self._directed[x]:
            del self._directed_dual[y][x]
        del self._directed[x]

        for y in self._directed_dual[x]:
            del self._directed[y][x]
        del self._directed_dual[x]

        for y in self._undirected[x]:
            del self._undirected[y][x]
        del self._undirected[x]

    def update(self, edges, kind, node_creation=True, delete=False):
        """Add/remove edges.

        Each edge in *edges* is either added or removed depending if it already present or not.

        If an edge is already present but not of the same type (undirected or directed), the edge is replaced even if
        delete is set to False.

        Args:
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).
            kind(str): either ``UNDIRECTED_EDGE`` or ``DIRECTED_EDGE``.
            node_creation(bool): If :const:`False`, edges using vertices not in the graph are discarded. If
                :const:`True`, missing vertices are added in the graph.
            delete(bool): If :const:`False` edges already present are not deleted from the graph.

        Raises:
            ValueError: if the two vertices of an edge are equal or if kind is unknown.
        """
        if kind == UNDIRECTED_EDGE:
            self.__update_undirected(edges, node_creation, delete)
        elif kind == DIRECTED_EDGE:
            self.__update_directed(edges, node_creation, delete)
        else:
            raise ValueError("Unknown edge type kind=%s" % (str(kind)))

        return self

    def __update_undirected(self, edges, node_creation=True, delete=False):
        """Add/remove undirected edges.

        Each edge in *edges* is either added or removed depending if it already present or not.

        If an edge is already a directed one, the undirected one replaces it.

        Args:
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).
            node_creation(bool): If :const:`False`, edges using vertices not in the graph are discarded. If
                :const:`True`, missing vertices are added in the graph.
            delete(bool): If :const:`False` edges already present are not deleted from the graph.

        """

        for x, y in edges:
            if (x not in self.vertices or y not in self.vertices) and not node_creation:
                continue

            if x not in self.vertices:
                self.add(x)
            if y not in self.vertices:
                self.add(y)

            if y in self._undirected[x] and delete:
                del self._undirected[x][y]
                del self._undirected[y][x]
            else:
                if y in self._directed[x]:
                    del self._directed[x][y]
                    del self._directed_dual[y][x]
                elif x in self._directed[y]:
                    del self._directed[y][x]
                    del self._directed_dual[x][y]

                self._undirected[x][y] = self._undirected[y][x] = None

        return self

    def __update_directed(self, edges, node_creation=True, delete=False):
        """Add/remove directed edges.

        Each edge in *edges* is either added or removed depending if it already present or not. If the edge is a
        triplet, it is only removed if the attributes coincide.

        If an edge is already a undirected one, the directed one replaces it.


        Args:
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).
            node_creation(bool): If :const:`False`, edges using vertices not in the graph are discarded. If
                :const:`True`, missing vertices are added in the graph.
            delete(bool): If :const:`False` edges already present are not deleted from the graph.

        Raises:
            ValueError: if the two vertices of an edge are equal.
        """

        for x, y in edges:
            if (x not in self.vertices or y not in self.vertices) and not node_creation:
                continue

            if x not in self.vertices:
                self.add(x)
            if y not in self.vertices:
                self.add(y)

            if y in self._directed[x] and delete:
                del self._directed[x][y]
                del self._directed_dual[y][x]
            else:
                if y in self._undirected[x]:
                    del self._undirected[x][y]
                    del self._undirected[y][x]
                self._directed[x][y] = self._directed_dual[y][x] = None

        return self

    def __len__(self):
        """Number of vertices."""

        return len(self.vertices)

    @property
    def nb_edges(self):

        return sum([len(self._directed[x]) for x in self.vertices]) \
               + .5 * sum([len(self._undirected[x]) for x in self.vertices])

    def degree(self, x):
        """number of undirected, and directed edge ending or begining in x.
        """
        return len(self._undirected[x]) + len(self._directed[x]) + len(self._directed_dual[x])

    def __iter__(self):
        """Iteration over the vertices."""

        for x in self.vertices:
            yield x

    def __getitem__(self, edge):
        """ Attribute of *edge*.

        Args:
            edge(couple): an edge.

        Raises:
            :exc:`ValueError` if edge is not an edge.

        returns:
            the attribute of the edge. `None` by default.
        """

        x, y = edge
        if y in self._undirected[x]:
            return self._undirected[x][y]
        elif y in self._directed[x]:
            return self._directed[x][y]
        else:
            raise ValueError("Not an edge")

    def __setitem__(self, edge, attribute):
        """Set the attribute of *edge*.

        Args:
            edge(couple): an edge.
            attribute: edge attribute.

        Raises:
            ValueError: if edge is not an edge.
        """
        x, y = edge
        if y in self._undirected[x]:
            self._undirected[x][y] = self._undirected[y][x] = attribute
        elif y in self._directed[x]:
            self._directed[x][y] = self._directed_dual[y][x] = attribute
        else:
            raise ValueError("Not an edge")

    def __call__(self, x, undirected=True, begin=True, end=True, closed=False):
        """Neighborhood of vertex x.

        Args:
            x: a vertex.
            undirected(bool): if True add undirected edges containing *x*
            begin(bool): if True add directed edges beginning with *x*
            end(bool): if True add directed edges ending with *x*
            closed(bool): if true adds *x* in the returns (closed neighborhood).

        Raises:
            ValueError: if *x* is not a vertex.

        Returns(frozenset):
            the neighbors of *x* according to the boolean specifications.

        """

        if x not in self.vertices:
            raise ValueError("Not a vertex")

        neighborhood = set()

        if closed:
            neighborhood.add(x)
        if undirected:
            neighborhood.update(self._undirected[x].keys())
        if begin:
            neighborhood.update(self._directed[x].keys())
        if end:
            neighborhood.update(self._directed_dual[x].keys())

        return frozenset(neighborhood)

    def isa_vertex(self, x):
        """Test if a vertex exists

        Args:
            x: a vertex to test.

        Returns(bool):
            True if *x* is a vertex, False otherwise.
        """

        return x in self._vertices

    def isa_edge(self, x, y, kind=None):
        """test if {x, y} or (x, y) is a edge.

        Args:
            x: a vertex.
            y: a vertex.
            kind: ``UNDIRECTED_EDGE``, ``UNDIRECTED_EDGE`` or `None` by default. Type of edge, both by default.

        Returns(bool):
            By default, returns True if {x, y} is or (x, y) is an edge, False otherwise. Kind of edge can be precised.
        """

        if kind == UNDIRECTED_EDGE:
            return y in self._undirected[x]
        elif kind == DIRECTED_EDGE:
            return y in self._directed[x]
        else:
            return y in self._undirected[x] or y in self._directed[x]

    def contraction(self, x, y, new_name=None):
        """Contract edge *xy*.

        If both an undirected and a directed edge should be added, result is unknown.

        Args:
            x: a vertex
            y: a vertex
            new_name: if set, the name of the new vertex, if not, the new name is *y*

        Raises:
            ValueError: if the new name is already a vertex different from x or y.
        """

        if new_name == x:
            x, y = y, x
        if new_name not in (x, y):
            self.add(new_name)

        for u in (x, y):
            self.update([(new_name, v) for v in
                         self(u, undirected=False, begin=True, end=False).difference([u == x and y or x])],
                        DIRECTED_EDGE, delete=False)
            self.update([(v, new_name) for v in
                         self(u, undirected=False, begin=False, end=True).difference([u == x and y or x])],
                        DIRECTED_EDGE, delete=False)
            self.update([(new_name, v) for v in
                         self(u, undirected=True, begin=False, end=False).difference([u == x and y or x])],
                        UNDIRECTED_EDGE, delete=False)

        self.remove(x)
        if new_name != y:
            self.remove(y)