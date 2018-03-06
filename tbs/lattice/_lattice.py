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

    def __eq__(self, other):
        return self._hase_diagram == other._hase_diagram

    def __iter__(self):
        for x in self._hase_diagram:
            yield x

    @property
    def hase_diagram(self):
        return DirectedGraph.from_graph(self._hase_diagram)

    @property
    def directed_comparability(self):
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

    def sup_filter(self, x):
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

    def inf_filter(self, x):
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
