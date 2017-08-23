from TBS.observer import Observable
from TBS.graph import Graph

__author__ = "cchatel"


class Lattice(Graph, Observable):
    """Lattice class seen as the oriented cover graph of the actual lattice"""

    def __init__(self, vertices=tuple(), edges=tuple(), dual=None):
        Observable.__init__(self)
        Graph.__init__(self, directed=True)
        if dual is None:
            self.dual_lattice = Lattice(dual=self)
        else:
            self.dual_lattice = dual
        self.attach(self.dual_lattice)
        self._neighborhood = {}

        for x in vertices:
            self._neighborhood[x] = {}

        if edges:
            self.update(edges)

    def update(self, edges=tuple(), node_creation=True, delete=True):
        """Add/remove edges and keep dual object up to date.

        Each edge in *edges* is either added or removed depending if it
        already present or not.

        :param edges: Each edge is a pair `(x, y)`
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
        Graph.update(self, edges, node_creation=True, delete=True)
        self.notify(edges)

    def dual_update(self, edges):
        """Add/remove edges in dual lattice.

        :param edges: Each edge is a pair `(x, y)`
        """
        Graph.update(self, ((y, x) for (x, y) in edges))

    def get_top(self):
        """Return the largest element.

        :param lattice: a lattice
        :type lattice: :class:`TBS.graph.Graph`

        :rtype: a element of the lattice.
        """
        for x in self:
            if not self[x]:
                return x

        return None

    def get_bottom(self):
        """Return the smallest element.

        :param lattice: a lattice
        :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

        :rtype: a element of the lattice.
        """

        return self.dual_lattice.get_top()

    def get_order(self):
        """Return the order associated with the lattice.

        :param lattice: a lattice
        :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

        :rtype: TBS.graph.Graph :class:`TBS.graph.Graph`
        """

        bottom = self.get_bottom()

        dual_order = Graph([bottom], directed=True)
        for vertex in self.topological_sort(bottom):
            for cover in self.dual_lattice[vertex]:
                dual_order.update([(vertex, cover)])
                dual_order.update([(vertex, y) for y in dual_order[cover]], delete=False)
        return dual_order.dual()

    def comparability_function(self):
        """Return a comparability function associated with the lattice.

        The return function takes two parameters and returns True if the first parameter is smaller than the second one
        for the given lattice.
        This function computes the lattice order (long). Should only be used for generic lattices where no other solution
        is avaliable.

        :param lattice: a lattice
        :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

        :rtype: function
        """
        lattice_order = self.get_order()

        def smaller_than(smaller, larger):
            """Comparability function.

            :param smaller: lattice element.
            :param larger: lattice element.

            :rtype: bool :class:`bool`
            """

            return larger in lattice_order[smaller]

        return smaller_than

    def inf_irreducible(self):
        """ Inf-irreductibles elements of the cover graph.

        :param lattice: a cover graph (may or may not have a bottom).
        :type lattice: :class:`TBS.graph.Graph`

        :return: the inf-irreducibles elements of *cover_graph*
        :rtype: :class:`frozenset`.
        """
        irreducible = set()
        for vertex in self:
            if len(self[vertex]) == 1:
                irreducible.add(vertex)

        return frozenset(irreducible)

    def sup_irreducible(self):
        """ Sup-irreductibles elements of the cover graph.

        :param cover_graph: a cover graph (may or may not have a top).
        :type cover_graph: :class:`TBS.graph.Graph`

        :return: the sup-irreducibles elements of *cover_graph*
        :rtype: :class:`frozenset`.
        """

        return self.dual_lattice.inf_irreducible()

    def sup_irreducible_clusters(self):
        """ Sup-irreducibles correspondance.

        :param lattice: a cover graph.
        :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

        :return: a dict associating each element to the sup-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        bottom = self.get_bottom()

        correspondance = {bottom: set()}

        for vertex in self.topological_sort(bottom):
            if vertex not in correspondance:
                correspondance[vertex] = set()
            if self.dual_lattice.isa_leaf(vertex):
                # sup_irreducible
                correspondance[vertex].add(vertex)
            for cover in self.dual_lattice[vertex]:
                correspondance[vertex].update(correspondance[cover])

        return {element: frozenset(sups) for element, sups in correspondance.items()}

    def inf_irreducible_clusters(self):
        """ Inf-irrerducibles correspondance.

        :param lattice: a cover graph.
        :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

        :return: a dict associating each element to the inf-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        return self.dual_lattice.sup_irreducible_clusters()
