from TBS.observer import Observable
from TBS.graph import Graph
import collections

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

    def remove(self, x):
        """Remove vertex in lattice

        :param x: Vertex to remove
        """
        Graph.remove(self, x)
        Graph.remove(self.dual_lattice, x)

    def get_top(self):
        """Return the largest element.

        :rtype: a element of the lattice.
        """
        for x in self:
            if not self[x]:
                return x

        return None

    def get_bottom(self):
        """Return the smallest element.

        :rtype: a element of the lattice.
        """

        return self.dual_lattice.get_top()

    def get_order(self):
        """Return the order associated with the lattice.

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

        :return: the sup-irreducibles elements of *cover_graph*
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

        :return: a dict associating each element to the inf-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        return self.dual_lattice.sup_irreducible_clusters()

    def sup_filter(self, element):
        """Return {y | y >= element}

        :param element: vertex of the lattice cover graph
        :type element: a vertex
        :rtype: :class:`frozenset`
        """

        element_filter = set()
        self.dfs(element, lambda vertex: element_filter.add(vertex))

        return frozenset(element_filter)

    def is_a_lattice(self):
        """Is the graph possible_lattice a lattice.

        :rtype: class:`bool`
        """

        elements = list(self)

        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                x = elements[i]
                y = elements[j]
                for graph in (self, self.dual_lattice):
                    filter_x = graph.sup_filter(x)
                    filter_y = graph.sup_filter(y)
                    unique_generator = False
                    intersection = filter_x.intersection(filter_y)
                    for possible_generator in intersection:
                        if graph.sup_filter(possible_generator) == intersection:
                            unique_generator = True
                            break
                    if not unique_generator:
                        return False
        return True

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
        if not self.path(u, v):
            self.update([(u, v)])

    def compute_height(self):
        """Index for vertices.

        if u covers v then index[u] < index[v]
        index[bottom] = 0 and for any u covering bottom index[u] = 1.

        :rtype: class:`dict`
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
