import random

__author__ = 'fbrucker'


class Graph(object):
    """Generic Graph class.
    """

    def __init__(self, vertices=tuple(), edges=tuple(), directed=False):
        """A graph G on *vertices* with no edges.

        :param vertices: Each vertex must be *hashable*.
        :type vertices: iterable

        :param directed: If :const:`True`, returns a :term:`directed graph`.
        :type directed: :class:`bool`

        :param edges: Each edge is either a pair `(x, y)` or a
                      triplet `(x, y, attr)` where *x* != *y* are vertices (in
                      *vertices* or not) and *attr* a not ``None``
                      object describing the edge *xy*.
        :type edges: iterable

        :rtype: :class:`Graph`
        """

        self._neighborhood = {}
        self._directed = directed

        for x in vertices:
            self._neighborhood[x] = {}

        if edges:
            self.update(edges)

    @classmethod
    def random_tree(cls, number_vertices):

        tree = Graph(directed=False)
        name_random = list(range(number_vertices))
        random.shuffle(name_random)
        for i in range(number_vertices - 1):
            x = name_random[i]
            y = name_random[random.randint(i + 1, number_vertices - 1)]
            tree.update(((x, y), ))

        return tree

    def __repr__(self):

        return "".join(["Graph(vertices=",
                        repr(list(self)),
                        ", edges=",
                        repr(self.edges(True)),
                        ", directed=",
                        repr(self.directed),
                        ")"])

    def __len__(self):
        """Number of vertices."""

        return len(self._neighborhood)

    def __iter__(self):
        """Iteration on the vertices of the graph."""

        for x in self._neighborhood:
            yield x

    @property
    def directed(self):
        """Directed status of the graph.

        .. warning:: If set from :const:`True` to :const:`False`, if
                    `(x, y)` is an edge, the edge `(y, x)` is added if
                    missing.

        :rtype: :class:`bool`
        """

        return self._directed

    @directed.setter
    def directed(self, boolean):
        """Change the directed status of the graph.

        :param boolean: directed if True, undirected otherwise.
        :type boolean: :class:`bool`
        """

        if boolean:
            self._directed = True
        else:
            for x, y in self._neighborhood.items():
                for z in y.keys():
                    if x not in self._neighborhood[z] or self._neighborhood[z][x] != self._neighborhood[x][z]:
                        self._neighborhood[z][x] = self._neighborhood[x][z]
            self._directed = False

    def __getitem__(self, x):
        """ Neighbors of *x*.

        :param x: a vertex.

        :raises: :exc:`ValueError` if *x* is not a vertex.

        :rtype: :class:`list`
        """

        if x not in self._neighborhood:
            raise ValueError("Not a vertex")

        return list(self._neighborhood[x])

    def __call__(self, x, y):
        """Attribute of edge xy.

        :raises: :exc:`ValueError` if *xy* is not an edge.
        """

        if x not in self._neighborhood or y not in self._neighborhood[x]:
            raise ValueError("Not an edge")

        return self._neighborhood[x][y]

    def update(self, edges=tuple(), node_creation=True, delete=False):
        """Add/remove edges.

        Each edge in *edges* is either added or removed depending if it
        already present or not. If the edge is a triplet, it is only removed
        if the attributes coincide.

        :param edges: Each edge is either a pair `(x, y)` or a
                      triplet `(x, y, attr)` where *x* != *y* are vertices (in
                      *vertices* or not) and *attr* a not ``None``
                      object describing the edge *xy*.
        :type edges: iterable

        :param node_creation: If :const:`False`, edges connecting vertices
                             not in the graph are discarded.
                             If :const:`True`, missing vertices are added
                             before adding the edge.
        :type node_creation:  :class:`bool`

        :param delete: If :const:`False` edges already present are not
                       deleted from the graph.
        :type delete: :class:`bool`

        :raises: :exc:`ValueError` if the two vertices of an edge are equal.
        """
        if not edges:
            edges = []

        for e in edges:
            if len(e) == 2:
                x, y = e
                attr = None
                no_attribute = True
            else:
                x, y, attr = e
                no_attribute = False

            if x == y:
                raise ValueError("Two identical vertices for edge %s" % (str(e)))
            if (x not in self._neighborhood or y not in self._neighborhood) and not node_creation:
                continue
            if x not in self._neighborhood:
                self._neighborhood[x] = {}
            if y not in self._neighborhood:
                self._neighborhood[y] = {}

            if y in self._neighborhood[x]:
                if delete and (no_attribute or self._neighborhood[x][y] == attr):
                    del self._neighborhood[x][y]
                    if not self.directed:
                        del self._neighborhood[y][x]
                else:
                    self._neighborhood[x][y] = attr
                    if not self.directed:
                        self._neighborhood[y][x] = attr
            else:
                self._neighborhood[x][y] = attr
                if not self.directed:
                    self._neighborhood[y][x] = attr
        return self

    def clear(self):
        """Delete all the edges of the graph."""

        for x in self._neighborhood:
            self._neighborhood[x] = {}

    def edges(self, attr=False):
        """
        :param attr: if :const:`True` returns a :class:`list` of triplets
                     `(x, y, attr)` where *attr* is the attribute of edge `xy`,
                     returns :class:`list` of of edges `(x, y)` otherwise.
        :type attr: :class:`bool`

        :rtype: :class:`list`

        .. warning:: each edge `xy` is represented only once (by `(x, y)` or
                     `(y, x)`). For a :term:`directed graph` nevertheless,
                     both couple may appear.
        """

        if self.directed:
            edges = [(x, y) for x in self._neighborhood for y in self._neighborhood[x]]
        else:
            edges = [tuple(A) for A in set([frozenset([x, y])
                                            for x in self._neighborhood for y in self._neighborhood[x]])]

        if attr:
            return [xy + (self(*list(xy)), ) for xy in edges]
        else:
            return edges

    def add(self, x):
        """Add vertex *x*.

        :param x: new vertex to add. Will be without neighbor.
        :raises: :exc:`ValueError` if *x* is already a vertex.
        """

        if x in self._neighborhood:
            raise ValueError("Already a vertex")

        self._neighborhood[x] = {}

    def contraction(self, x, y):
        """The neighbors of *x* become neighbors of *y* and delete *x*.

        :param x: a vertex.
        :param y: a vertex.
        """

        for z in self[x]:
            if y != z:
                self.update([(y, z, self(x, z))], delete=False)
        if self.directed:
            for z in self:
                if z in (x, y):
                    continue
                if self.isa_edge(z, x) and z != y:
                    self.update([(z, y, self(z, x))], delete=False)

        self.remove(x)

    def remove(self, x):
        """Remove vertex *x*.

        :param x: a vertex.

        :raises: :exc:`ValueError` if *x* is not a vertex.
        """

        if x not in self._neighborhood:
            raise ValueError("Not a vertex")

        for y in self._neighborhood:
            if y == x:
                continue

            if x in self._neighborhood[y]:
                del self._neighborhood[y][x]
        del self._neighborhood[x]

    def rename(self, x, newx):
        """Rename element *x* to *newx*.

        :param x: vertex
        :param newx: the replacing element

        :raises: :exc:`ValueError` if either *x* is not a vertex or
                 *newx* is already one.
        """

        if (x not in self._neighborhood) or (newx in self._neighborhood):
            raise ValueError("Vertex already present or removing a non-element.")

        for y in self._neighborhood:
            if y == x:
                continue
            if x in self._neighborhood[y]:
                self._neighborhood[y][newx] = self._neighborhood[y][x]
                del self._neighborhood[y][x]
        self._neighborhood[newx] = self._neighborhood[x]
        del self._neighborhood[x]

    def restriction(self, vertex_subset=None):
        """Restriction to *Y*.

        :param vertex_subset: subset of self's vertex set. If ``None``, Y is considered
                  to be the whole vertex set.
        :type vertex_subset: iterable

        :rtype: :class:`Graph`
        """

        if not vertex_subset:
            vertex_subset = list(self)

        g = self.__class__(vertex_subset, directed=self.directed)
        g.update(self.edges(True), False)

        return g

    def copy(self):
        """Deep copy.

        Copy the structure. Attributes and vertices remains the same.

        :rtype: tbs.graph.Graph :class:`tbs.graph.Graph`
        """

        return self.restriction()

    def dual(self):
        """Dual graph.

        :rtype: tbs.graph.Graph :class:`tbs.graph.Graph`
        """

        return Graph(self, directed=self.directed).update([(y, x, attr) for x, y, attr in self.edges(True)])

    def __nonzero__(self):
        """False if no vertex."""

        if self._neighborhood:
            return True
        return False

    def __eq__(self, g):
        """Same vertices, same egdes and same attribute for each edge."""

        return self.directed == g.directed and \
            set([frozenset(self[x]) for x in self]) == set([frozenset(g[x]) for x in g])

    def __ne__(self, g):
        """not ==."""

        return not self == g

    def isa_vertex(self, x):
        """Test if a vertex exists

        :param x: a vertex to test.

        :rtype: :class:`bool`
        """

        return x in self._neighborhood

    def isa_edge(self, x, y):
        """test if (x, y) is an edge.

        :param x: a vertex.
        :param y: a vertex.

        :rtype: :class:`bool`
        """

        return x in self._neighborhood and y in self._neighborhood[x]

    def isa_leaf(self, x):
        """*x* has 1 neighbor.

        :param x: a vertex.
        :rtype: :class:`bool`
        """

        return self.degree(x) == 1

    def degree(self, x, out=True):
        """Number of neighbors of vertex *x*.

        For directed graphs, only gives the number of vertices which go out
        the vertex.

        :param x: a vertex.

        :param out: If :const:`False` return the number of vertices which
                   end at the vertex. Only for directed graphs.
        :type out: :class:`bool`
        """

        if not self.directed or out:
            return len(self._neighborhood[x])
        else:
            nb = 0
            for y in self:
                if x == y:
                    continue
                if self.isa_edge(y, x):
                    nb += 1
            return nb

    def nb_edges(self):

        nb = sum([len(self._neighborhood[x]) for x in self._neighborhood])

        if self.directed:
            return nb
        else:
            return nb / 2

