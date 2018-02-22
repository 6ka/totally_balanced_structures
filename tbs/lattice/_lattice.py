from tbs.observer import Observable
from tbs.graph import Graph, dfs, topological_sort, path
import collections

__author__ = "cchatel", "fbrucker"


class Lattice(Graph, Observable):
    """
    Lattice class seen as the oriented cover graph of the actual lattice
    """

    def __init__(self, vertices=tuple(), edges=tuple(), dual=None):
        """Creates a lattice object with vertices vertices and edges edges.

        :param vertices: a tuple of vertices to initialize the lattice
        :type vertices: iterable
        :param edges: a tuple of edges to initialize the lattice
        :type edges: iterable
        :param dual: used to maintain dual up to date, not to be used
        :type dual: :class:`tbs.lattice.Lattice`
        """

        Observable.__init__(self)
        Graph.__init__(self, directed=True)
        if dual is None:
            self.dual_lattice = self.__class__(dual=self)
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
        :type edges: iterable
        """
        Graph.update(self, ((y, x) for (x, y) in edges), delete=True)

    def remove(self, x):
        """Remove vertex in lattice

        :param x: name of the vertex to remove
        """
        Graph.remove(self, x)
        Graph.remove(self.dual_lattice, x)

    def get_top(self):
        """Return the largest element.

        :rtype: an element of the lattice.
        """
        for x in self:
            if not self[x]:
                return x

        return None

    def get_bottom(self):
        """Return the smallest element.

        :rtype: an element of the lattice.
        """

        return self.dual_lattice.get_top()

    def get_order(self):
        """Return the order associated with the lattice.

        :rtype: tbs.graph.Graph :class:`tbs.graph.Graph`
        """

        bottom = self.get_bottom()

        dual_order = Graph([bottom], directed=True)
        for vertex in topological_sort(self, bottom):
            for cover in self.dual_lattice[vertex]:
                dual_order.update([(vertex, cover)])
                dual_order.update([(vertex, y) for y in dual_order[cover]], delete=False)
        return dual_order.dual()

    def comparability_function(self):
        """Return a comparability function associated with the lattice.

        The return function takes two parameters and returns True if the first parameter is smaller than the second one
        for the given lattice.
        This function computes the lattice order (long). Should only be used for generic lattices where no other solution
        is available.

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
        """ Inf-irreductibles elements of the lattice.

        :return: the inf-irreducibles elements of the lattice
        :rtype: :class:`frozenset`.
        """
        irreducible = set()
        for vertex in self:
            if len(self[vertex]) == 1:
                irreducible.add(vertex)

        return frozenset(irreducible)

    def sup_irreducible(self):
        """ Sup-irreductibles elements of the lattice.

        :return: the sup-irreducibles elements of the lattice
        :rtype: :class:`frozenset`.
        """

        return self.dual_lattice.inf_irreducible()

    def sup_irreducible_clusters(self):
        """ Sup-irreducibles correspondance.

        :return: a dict associating each element to the sup-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        bottom = self.get_bottom()

        correspondance = {bottom: set()}

        for vertex in topological_sort(self, bottom):
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

        :return: a dict associating each element to the inf-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        return self.dual_lattice.sup_irreducible_clusters()

    def sup_filter(self, element):
        """Return {y | y >= element}

        :param element: vertex of the lattice
        :type element: a vertex
        :rtype: :class:`frozenset`
        """

        element_filter = set()
        dfs(self, element, lambda vertex: element_filter.add(vertex))

        return frozenset(element_filter)


    def delete_join_irreducible(self, join_irreducible):
        """Delete a join irreducible element from lattice.

        :param join_irreducible: a join irreducible element from the lattice.
        """
        v = self[join_irreducible][0]
        u = None
        for u in self:
            if join_irreducible in self[u]:
                break

        self.remove(join_irreducible)
        if not path(self, u, v):
            self.update([(u, v)])

    def compute_height(self):
        """Index for vertices.

        if u covers v then index[u] < index[v]
        index[bottom] = 0 and for any u covering bottom index[u] = 1.

        :rtype: :class:`dict`
        """

        bottom = self.get_bottom()

        number_remaining_predecessors = {}
        for u, v in self.edges():
            number_remaining_predecessors[v] = number_remaining_predecessors.get(v, 0) + 1

        height = {bottom: 0}

        fifo = collections.deque((bottom,))
        while fifo:
            vertex = fifo.pop()
            for neighbor in self[vertex]:
                number_remaining_predecessors[neighbor] -= 1
                if not number_remaining_predecessors[neighbor]:
                    height[neighbor] = height[vertex] + 1
                    fifo.appendleft(neighbor)

        return height

    def sup(self, element, other_element):
        """Computes the sup of two elements

        :param element: a vertex of the lattice
        :param other_element: another vertex of the lattice
        :return: the element which is the sup of element and other_element
        """
        element_sup = self.sup_filter(element)
        other_element_sup = self.sup_filter(other_element)
        intersection_sup = element_sup.intersection(other_element_sup)
        for element in intersection_sup:
            if not frozenset(self.dual_lattice[element]).intersection(intersection_sup):
                return element

    def inf(self, element, other_element):
        """Computes the inf of two elements

        :param element: a vertex of the lattice
        :param other_element: another vertex of the lattice
        :return: the element which is the inf of element and other_element
        """
        return self.dual_lattice.sup(element, other_element)

    def atoms(self):
        """Returns atoms of the lattice

        :return: set of vertices
        """
        bottom = self.get_bottom()
        return set(self[bottom])

    def make_atomistic(self):
        """Makes the lattice atomistic i.e all objects are atoms.
        """
        sup_irr = self.sup_irreducible()
        bottom = self.get_bottom()
        atoms = self.atoms()
        current_element_index = len(self) - 1
        for sup in sup_irr:
            if sup not in atoms:
                self.update(((bottom, current_element_index), (current_element_index, sup)))
                current_element_index += 1

    def is_atomistic(self):
        """Check whether the lattice is atomistic or not

        :rtype: :class:`bool`
        """
        return self.atoms() == self.sup_irreducible()


