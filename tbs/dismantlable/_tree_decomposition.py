import random

from ..graph import DirectedGraph
from ._binary_mixed_tree import BinaryMixedTree


class DecompositionBTB:
    """
    Tree decomposition of binary lattices.
    """

    def __init__(self, initial_tree):
        """Creates a decomposition beginning from an initial_tree and a lattice if needed.
        
        :param initial_tree: the tree to begin with
        :type initial_tree: class:`tbs.graph.Graph`
        """
        self.tree = BinaryMixedTree(initial_tree)
        self.history = []
        self.order = []
        self.hase_diagram = DirectedGraph()
        for x in initial_tree:
            self.hase_diagram.update(((frozenset(), frozenset({x})),))
        self.store()

    def store(self):
        self.history.append(self.tree.copy())

    @classmethod
    def build_from_tree(cls, initial_tree):
        """Creates a decomposition of a binary lattice (found in self.history) and the associated lattice (self.lattice)
        """

        def random_choice(u):
            population = list(self.tree(u, undirected=True, begin=False, end=False))
            random.shuffle(population)
            k = random.randint(0, len(population))

            return population[:k]

        self = cls(initial_tree)

        while len(self.tree) > 1:
            x, y = self.tree.get_edge()
            self.step(x, y, random_choice)
            self.order.append((x, y))
            self.store()
            self.hase_diagram.update(((x, x.union(y)), (y, x.union(y))))

        return self

    def step(self, x, y, neighbor_move):
        xy = self.tree.add_union(x, y)

        for u in (x, y):

            other_successor = self.tree.get_other_successor_or_none(u, xy)

            if other_successor:
                self.tree.add_undirected(xy, other_successor)
                self.tree.remove_directed(u, other_successor)
                self.tree.move_undirected_from_to(u, xy)
                self.tree.move_directed_from_to(u, xy)

            else:
                self.tree.move_undirected_from_to(u, xy, neighbor_move(u))

            if len(self.tree(u, undirected=True, begin=False, end=False)) == 0:
                self.tree.move_directed_from_to(u, xy)
                self.tree.remove(u)

    @classmethod
    def build_from_binary_lattice(cls, lattice):
        """Decomposes a lattice.

        :param lattice: the binary lattice to decompose
        :type lattice: class: `tbs.lattice.Lattice`
        :param order: an order to build the lattice. If None, a compatible order is computed.
        :type order: iterable
        """

        tree = lattice.support_tree()
        self = cls(tree)
        cluster_to_vertex = {frozenset({x}): x for x in tree}
        vertex_to_cluster = {x: frozenset({x}) for x in tree}

        for vertex in lattice.decomposition_order():
            x_vertex, y_vertex = list(lattice.under(vertex))
            x = vertex_to_cluster[x_vertex]
            y = vertex_to_cluster[y_vertex]
            cluster_to_vertex[x.union(y)] = vertex
            vertex_to_cluster[vertex] = x.union(y)

            def sup_choice(u):
                population = {cluster_to_vertex[x] for x in self.tree(u, undirected=True, begin=False, end=False)}

                return {vertex_to_cluster[v] for v in population
                        if lattice.is_smaller_than(vertex, lattice.sup(v, cluster_to_vertex[u]))}

            self.step(x, y, sup_choice)
            self.order.append((x, y))
            self.store()
            self.hase_diagram.update(((x, x.union(y)), (y, x.union(y))))

        return self

