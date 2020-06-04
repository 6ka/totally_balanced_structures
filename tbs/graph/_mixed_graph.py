import json

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
            directed_edges(iterable): list of pair (x, y) where *x* and *y* are vertices.
            undirected_edges(iterable): same as directed_edges for undirected edges. Undirected edges replace directed
                one if they already exist.

        edges using vertices not in the graph are discarded.
        One Cannot have both (x, y) as undirected and directed edge.
        """

        self._vertices = frozenset()
        self._undirected = dict()  # x - y means y in dict[x] and x in dict[y]
        self._directed = dict()  # x -> y means y in dict[x]
        self._directed_dual = dict()  # x -> y means x in dict[y]

        for x in vertices:
            self.add(x)

        self.__update_directed(directed_edges, node_creation=False)
        self.__update_undirected(undirected_edges, node_creation=False)

    @classmethod
    def from_graph(cls, graph, vertices=None):
        """Create graph from another graph.

        Args:
            graph(MixedGraph): a mixed graph
            vertices: a subset of vertices. If not set, the whole set of vertices is considered.

        Returns(MixedGraph): A new graph
        """

        undirected, directed = graph._edges
        if vertices is None:
            vertices = graph.vertices

        return cls(vertices, undirected, directed)

    @staticmethod
    def _graph_parts_from_json(json_graph, id_to_vertex_conversion):
        g_son = json_graph["graph"]
        vertices = [id_to_vertex_conversion(x["id"]) for x in g_son["nodes"]]

        undirected = []
        directed = []

        for edge in g_son["edges"]:
            x = id_to_vertex_conversion(edge["source"])
            y = id_to_vertex_conversion(edge["target"])

            if "directed" in edge:
                if edge["directed"]:
                    directed.append((x, y))
                else:
                    undirected.append((x, y))
            elif "directed" in g_son:
                if g_son["directed"]:
                    directed.append((x, y))
                else:
                    undirected.append((x, y))
        return vertices, undirected, directed

    @classmethod
    def from_json(cls, json_graph, id_to_vertex_conversion=json.loads):
        """jsgongraph to mixed-graph


        Args:
            json_graph(dict):  https://github.com/jsongraph format.
            id_to_vertex_conversion(str->object): each id is converterted into a vertex = id_to_vertex_conversion(id).
                    By defaults, node ids are json.loads() to produce vertices. Thus if the node id is "1"
                    the associated vertex s the int 1.

        Returns(MixedGraph): the mixed graph associated with the json
        """

        vertices, undirected, directed = cls._graph_parts_from_json(json_graph, id_to_vertex_conversion)
        return cls(vertices, undirected, directed)

    def __repr__(self):
        undirected, directed = self.edges
        return "".join(["MixedGraph(",
                        repr(self.vertices),
                        ", ", repr(undirected),
                        ", ", repr(directed),
                        ")"])

    def json(self):
        """Jsongraph format.

        https://github.com/jsongraph

        node ids are string. Thus it's the json.dumps of the vertices.

        returns(dict): jsongraph format of the graph
        """

        vertices = list(self)
        index = {vertices[i]: i for i in range(len(vertices))}

        json_graph = {
            "nodes": [
                {
                    "id": json.dumps(x)
                }
                for x in self
            ],
            "edges": [
                         {
                             "source": json.dumps(x),

                             "target": json.dumps(y),
                             "directed": True,
                         }
                         for x in self._directed for y in self._directed[x]

                     ] + [
                         {
                             "source": json.dumps(x),

                             "target": json.dumps(y),
                             "directed": False,
                         }
                         for x in self._undirected for y in self._undirected[x] if index[y] >= index[x]
                     ]

        }

        return {"graph": json_graph}

    @property
    def vertices(self):
        """Vertex set."""

        return self._vertices

    @property
    def _edges(self):
        """Undirected and directed edges.

        returns:
            A couple (U, D) where U is a :class:`frozenset` of 2-element frozenset (the undirected edges) and D is a
            frozenset of 2-element tuple (the directed edges).
        """

        return [frozenset(frozenset([x, y]) for x, Y in self._undirected.items() for y in Y),
                frozenset((x, y) for x, Y in self._directed.items() for y in Y)]

    @property
    def edges(self):
        """Undirected and directed edges.

        returns:
            A couple (U, D) where U is a :class:`frozenset` of 2-element frozenset (the undirected edges) and D is a
            frozenset of 2-element tuple (the directed edges).
        """

        return self._edges

    def __nonzero__(self):
        """False if no vertex."""

        if self._vertices:
            return True
        return False

    def __eq__(self, g):
        """Same vertices, same egdes and same attribute for each edge."""

        return self.vertices == g.vertices and self._edges == g._edges

    def __ne__(self, g):
        """not ==."""

        return not self == g

    def __contains__(self, vertex):
        """is a vertex"""

        return vertex in self.vertices

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

    def difference(self, edges):
        """Remove edges.

        Each edge in *edges* is removed from the graph.

        Args:
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).

        Returns:
            self (for possible chaining).
        """

        for x, y in edges:
            if x not in self.vertices or y not in self.vertices:
                continue

            if y in self._undirected[x]:
                del self._undirected[x][y]
                del self._undirected[y][x]
            elif y in self._directed[x]:
                del self._directed[x][y]
                del self._directed_dual[y][x]

        return self

    def update(self, kind, edges, node_creation=True):
        """Add edges.

        Each edge in *edges* is added if not already present.

        If an edge is already present but not of the same type (undirected or directed), the edge is replaced.

        Args:
            kind(str): either ``UNDIRECTED_EDGE`` or ``DIRECTED_EDGE``.
            edges(iterable): Each edge is a pair `(x, y)` where *x* != *y* are vertices (in *vertices* or not).
            node_creation(bool): If :const:`False`, edges using vertices not in the graph are discarded. If
                :const:`True`, missing vertices are added in the graph.

        Raises:
            ValueError: if kind is unknown.
        Returns:
            self (for possible chaining).
        """

        if kind == UNDIRECTED_EDGE:
            self.__update_undirected(edges, node_creation)
        elif kind == DIRECTED_EDGE:
            self.__update_directed(edges, node_creation)
        else:
            raise ValueError("Unknown edge type kind=%s" % (str(kind)))

        return self

    def __update_undirected(self, edges, node_creation=True):
        for x, y in edges:
            if (x not in self.vertices or y not in self.vertices) and not node_creation:
                continue

            if x not in self.vertices:
                self.add(x)
            if y not in self.vertices:
                self.add(y)

            if y in self._undirected[x]:
                continue

            if y in self._directed[x]:
                del self._directed[x][y]
                del self._directed_dual[y][x]
            elif x in self._directed[y]:
                del self._directed[y][x]
                del self._directed_dual[x][y]

            self._undirected[x][y] = self._undirected[y][x] = None

        return self

    def __update_directed(self, edges, node_creation=True):
        for x, y in edges:
            if (x not in self.vertices or y not in self.vertices) and not node_creation:
                continue

            if x not in self.vertices:
                self.add(x)
            if y not in self.vertices:
                self.add(y)

            if y in self._directed[x]:
                continue

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

    def __call__(self, x, undirected=True, begin=True, end=False, closed=False):
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
            self.update(DIRECTED_EDGE,
                        [(new_name, v) for v in
                         self(u, undirected=False, begin=True, end=False).difference([u == x and y or x])])
            self.update(DIRECTED_EDGE,
                        [(v, new_name) for v in
                         self(u, undirected=False, begin=False, end=True).difference([u == x and y or x])])
            self.update(UNDIRECTED_EDGE,
                        [(new_name, v) for v in
                         self(u, undirected=True, begin=False, end=False).difference([u == x and y or x])])

        self.remove(x)
        if new_name != y:
            self.remove(y)

    def path(self, x, y, valuation=lambda u, v: 1, forbidden_vertices=frozenset()):
        """A minimal path (according to f) from *x* to *y*.

        Bellman-ford algorithm.

        Args:
            u: vertex
            v: vertex
            valuation(u, v -> value): associates the edge u, v to a real number.
            forbidden_vertices(iterable): set of vertices which are not in the path
        Returns(list):
            a minimal path from x to y.
       """

        k = 0
        n = len(self)

        father = {x: x}
        dist = {x: 0}
        change = True

        while k < n and change:
            change = False
            k += 1
            for u in self:
                for v in self(u):
                    if v in forbidden_vertices:
                        continue
                    if u in dist and (v not in dist or dist[v] > dist[u] + valuation(u, v)):
                        dist[v] = dist[u] + valuation(u, v)
                        father[v] = u
                        change = True

        if change:
            raise Exception("Absorbent circuit")

        if y not in father:
            return []

        path = []
        current = y

        while current != x:
            path.append(current)
            current = father[current]
        path.append(x)
        path.reverse()

        return path
