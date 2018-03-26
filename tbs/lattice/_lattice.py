__author__ = "cchatel", "fbrucker"

from ..graph import DirectedGraph, \
    direct_comparability_graph_to_hase_diagram, direct_acyclic_graph_to_direct_comparability_graph


class Lattice:
    """Lattice class."""

    def __init__(self, dag=None):
        """Creates a lattice object from a direct acyclic graph.

        There is no verification whether dag is a Lattice order or not.

        Args:
            dag(DirectedGraph): A directed acyclic graph associated with a lattice order.
        """

        if dag is None:
            dag = DirectedGraph()

        self._order = direct_acyclic_graph_to_direct_comparability_graph(dag)
        self._hase_diagram = direct_comparability_graph_to_hase_diagram(self._order)

        self._top = self._get_top()
        self._bottom = self._get_bottom()

    def _get_top(self):
        for x in self._hase_diagram:
            if not self._hase_diagram(x):
                return x
        return None

    def _get_bottom(self):
        for x in self._hase_diagram:
            if not self._hase_diagram(x, begin=False, end=True):
                return x
        return None

    @classmethod
    def from_lattice(cls, lattice):
        new_lattice = cls()

        new_lattice._hase_diagram = DirectedGraph.from_graph(lattice._hase_diagram)
        new_lattice._order = DirectedGraph.from_graph(lattice._order)
        new_lattice._top = lattice._top
        new_lattice._bottom = lattice._bottom

        return new_lattice

    def __eq__(self, other):
        return self._hase_diagram == other._hase_diagram

    def __iter__(self):
        for x in self._hase_diagram:
            yield x

    def __len__(self):
        return len(self._hase_diagram)

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self._hase_diagram) + ")"

    def __str__(self):
        return repr(self)

    @property
    def hase_diagram(self):
        """Return a copy of the lattice hase diagram."""
        return DirectedGraph.from_graph(self._hase_diagram)

    @property
    def directed_comparability(self):
        """Return a copy of the lattice directed comparability graph (with no loop)."""
        return DirectedGraph.from_graph(self._order)

    @property
    def top(self):
        """Largest element."""

        return self._top

    @property
    def bottom(self):
        """Smallest element."""
        return self._bottom

    def sup(self, x, y):
        """x v y

        Args:
            x: a vertex
            y: a vertex

        Returns:
            The sup of x and y
        """
        sup = None

        for z in self._order(x, closed=True):
            if y == z or self._order.isa_edge(y, z):
                if sup is None or self._order.isa_edge(z, sup):
                    sup = z

        return sup

    def above(self, x):
        """upper cover elements of x

        Args:
            x: a vertex

        Returns(frozenset):
            The successors of x in the hase diagram.
        """
        return self._hase_diagram(x)

    def above_filter(self, x):
        """{y | y >= x}

        Args:
            x: vertex

        Returns(frozenset):
            {y | y >= x}
        """

        return self._order(x, closed=True)

    def inf(self, x, y):
        """x ^ y

        Args:
            x: a vertex
            y: a vertex

        Returns:
            The inf of x and y
        """
        inf = None

        for z in self._order(x, begin=False, end=True, closed=True):
            if z == y or self._order.isa_edge(z, y):
                if inf is None or self._order.isa_edge(inf, z):
                    inf = z

        return inf

    def is_smaller_than(self, x, y):
        """ x < y ?

        Args:
            x, y: vertex

        Returns(bool):
            True if x < y, False otherwise
        """
        return self._order.isa_edge(x, y)

    def is_larger_than(self, x, y):
        """ x > y ?

        Args:
            x, y: vertex

        Returns(bool):
            True if x > y, False otherwise
        """
        return self._order.isa_edge(y, x)

    def under(self, x):
        """lower cover elements of x

        Args:
            x: a vertex

        Returns(frozenset):
            The predecessors of x in the hase diagram.
        """
        return self._hase_diagram(x, begin=False, end=True)

    def under_filter(self, x):
        """{y | y <= x}

        Args:
            x: vertex

        Returns(frozenset):
            {y | y <= x}
        """

        return self._order(x, begin=False, end=True, closed=True)

    @property
    def inf_irreducible(self):
        """ Inf-irreductible elements of the lattice.

        Returns(frozenset):
            the inf-irreducible elements of the lattice
        """
        return frozenset(x for x in self if len(self._hase_diagram(x)) == 1)

    @property
    def sup_irreducible(self):
        """ Sup-irreducible elements of the lattice.

        Returns(frozenset):
            the sup-irreducible elements of the lattice
        """
        return frozenset(x for x in self if len(self._hase_diagram(x, begin=False, end=True)) == 1)

    @property
    def join_irreducible(self):
        """ join-irreducible elements of the lattice.

        Returns(frozenset):
            the join-irreducible elements of the lattice
        """

        return frozenset(x for x in self
                         if len(self._hase_diagram(x)) == 1 and len(self._hase_diagram(x, begin=False, end=True)) == 1)

    def add_join_irreducible(self, new, u, v):
        """ Add a join irreducible element x to the lattice.

            Args:
                new: new element.
                u, v: two vertices such that u and v are different and comparable.

            If the lattice has no elements then u = v = None and if te lattice has 1 element u or v is None (thus
            either new becomes bottom or top).

            Raises(TypeError): if x is in the lattice, u == v or u and v are not comparable.

            Returns: self
        """
        if len(self._hase_diagram) == 0:
            self._hase_diagram.add(new)
            self._order.add(new)
            self._top = self._bottom = new
            return self

        if new in self._hase_diagram:
            raise TypeError("new element already in lattice")
        if u == v or new == u or new == v:
            raise TypeError("two elements are equal")

        if len(self._hase_diagram) == 1:
            if u is None:
                self._hase_diagram.update([(new, v)])
                self._order.update([(new, v)])
                self._bottom = new
            elif v is None:
                self._hase_diagram.update([(u, new)])
                self._order.update([(u, new)])
                self._top = new
            return self

        if u not in self._hase_diagram or v not in self._hase_diagram:
            raise TypeError("last elements must be in the lattice")
        if not self._order.isa_edge(u, v) and not self._order.isa_edge(v, u):
            raise TypeError("elements must be comparable")

        if not self._order.isa_edge(u, v):
            u, v = v, u

        if self._hase_diagram.isa_edge(u, v):
            self._hase_diagram.difference([(u, v)])

        self._hase_diagram.update([(u, new), (new, v)])
        self._order.update([(u, new), (new, v)])
        self._order.update((new, w) for w in self._order(v))
        self._order.update((w, new) for w in self._order(u, begin=False, end=True))

        return self

    def make_atomistic(self, new_name=lambda lattice, sup_not_atom: len(lattice)):
        """Makes the lattice atomistic.

        Make All sup-irreducible elements (objects) atoms. Iteratively checks the sup-irreductible elements and add new
        ones.

        Args:
            new_name(self, elements -> hashable): new name generator. Take the actual lattice and the current non atom
                sup-irreducible element in argument and return a new element not already in the lattice.
                By default use the length of the lattice.
        Returns:
            self
        """

        for x in self.sup_irreducible:
            if not self._hase_diagram.isa_edge(self.bottom, x):
                self.add_join_irreducible(new_name(self, x), self.bottom, x)

        return self

    def make_co_atomistic(self, new_name=lambda lattice, inf_not_co_atom: len(lattice)):
        """Makes the lattice co-atomistic.

        Make All inf-irreducible elements (attributes) co-atoms. Iteratively checks the inf-irreductible elements and
        add new ones.

        Args:
            new_name(self, elements -> hashable): new name generator. Take the actual lattice and the current non atom
                inf-irreducible element in argument and return a new element not already in the lattice.
                By default use the length of the lattice.
        Returns:
            self
        """

        for x in self.inf_irreducible:
            if not self._hase_diagram.isa_edge(x, self.top):
                self.add_join_irreducible(new_name(self, x), x, self.top)
        return self

    def is_atomistic(self):
        """Check whether the lattice is atomistic or not."""
        return self.above(self.bottom) == self.sup_irreducible

    def is_co_atomistic(self):
        """Check whether the lattice is co-atomistic or not."""
        return self.under(self.top) == self.inf_irreducible
