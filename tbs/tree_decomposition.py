import random

from .dismantlable_lattice import DismantlableLattice
from .graph.binary_mixed_tree import BinaryMixedTree


def tree_decomposition_of_binary_lattice(binary_lattice, order=None):
    """Returns an object representing a family of trees creating all the vertices of the lattice.

    :param order: an order to create vertices
    :type order: iterable

    :return: a decomposition
    :rtype: :class:`tbs.tree_decomposition.DecompositionBTB`
    """
    tree = binary_lattice.support_tree()
    if not order:
        order = iter(binary_lattice.decomposition_order())
    decomposition = DecompositionBTB(tree)
    decomposition.build_from_lattice(binary_lattice, order)
    return decomposition


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
        self.lattice = DismantlableLattice()
        for x in initial_tree:
            self.lattice.update((("BOTTOM", str(frozenset({x}))), ))
        self.store()

    def store(self):
        self.history.append(self.tree.copy())

    def build_binary_lattice(self):
        """Creates a decomposition of a binary lattice (found in self.history) and the associated lattice (self.lattice)
        """
        while len(self.tree) > 1:
            x, y = self.tree.get_edge()
            self.step(x, y)
            self.order.append((x, y))
            self.store()
            self.lattice.update(((str(x), str(x.union(y))), (str(y), str(x.union(y)))))

    def step(self, x, y):
        xy = self.tree.add_union(x, y)

        for u in (x, y):
            other_successor = self.tree.get_other_successor_or_none(u, xy)

            if other_successor:
                self.tree.add_undirected(xy, other_successor)
                self.tree.remove_directed(u, other_successor)
                self.tree.move_undirected_from_to(u, xy)
                self.tree.move_directed_from_to(u, xy)
            else:
                self.tree.move_undirected_from_to(u, xy, self.random_choice(u))

            if len(self.tree(u, undirected=True, begin=False, end=False)) == 0:
                self.tree.move_directed_from_to(u, xy)
                self.tree.remove(u)

    def random_choice(self, u):
        population = list(self.tree(u, undirected=True, begin=False, end=False))
        random.shuffle(population)
        k = random.randint(0, len(population))

        return population[:k]

    def build_from_lattice(self, lattice, order=None):
        """Decomposes a lattice.
        
        :param lattice: the lattice to decompose
        :type lattice: class: `tbs.lattice.Lattice`
        :param order: an order to build the lattice. If None, a compatible order is computed.
        :type order: iterable
        """
        self.lattice = lattice
        if not order:
            order = iter(lattice.decomposition_order())
        clusters = self.lattice.sup_irreducible_clusters()
        already_created = set()
        for vertex in order:
            self.contract_tree_edge_from_lattice(vertex, already_created, lattice)
            already_created.add(vertex)
            self.store()
            pred1, pred2 = self.lattice.dual_lattice[vertex][0], self.lattice.dual_lattice[vertex][1]
            self.order.append((clusters[pred1], clusters[pred2]))

    def contract_tree_edge_from_lattice(self, class_to_create, already_created, lattice):
        clusters = lattice.sup_irreducible_clusters()
        lattice_index_correspondance = {clusters[x]: x for x in clusters}
        dual = lattice.dual_lattice
        already_created.add(class_to_create)
        pred1, pred2 = clusters[dual[class_to_create][0]], clusters[dual[class_to_create][1]]
        self.tree.remove_undirected(pred1, pred2)
        self.tree.add(clusters[class_to_create])
        for predecessor in dual[class_to_create]:
            if len(lattice[predecessor]) == 1:
                self.tree.move_undirected_from_to(clusters[predecessor], clusters[class_to_create])
                for directed_neighbour in self.tree(clusters[predecessor], undirected=False, begin=True, end=False):
                    self.tree.add_undirected(directed_neighbour, clusters[class_to_create])
                self.tree.remove(clusters[predecessor])
            elif len(lattice[predecessor]) == 2:
                if lattice[predecessor][0] == class_to_create:
                    other_succ = lattice[predecessor][1]
                elif lattice[predecessor][1] == class_to_create:
                    other_succ = lattice[predecessor][0]
                else:
                    raise ValueError("Lattice is not binary")
                if other_succ not in already_created:
                    self.tree.add_directed(clusters[predecessor], clusters[class_to_create])
                    neighbours_at_beginning = self.tree(clusters[predecessor], undirected=True, begin=False, end=False).copy()
                    for undirected_neighbour in neighbours_at_beginning:
                        if lattice.sup_filter(lattice_index_correspondance[undirected_neighbour]).intersection(
                                        lattice.sup_filter(predecessor)) <= lattice.sup_filter(class_to_create):
                            self.tree.remove_undirected(undirected_neighbour, clusters[predecessor])
                            self.tree.add_undirected(undirected_neighbour, clusters[class_to_create])
                else:
                    self.tree.move_undirected_from_to(clusters[predecessor], clusters[class_to_create])
                    self.tree.add_undirected(clusters[other_succ], clusters[class_to_create])
                    self.tree.remove(clusters[predecessor])
            else:
                raise ValueError("Lattice is not binary")

    def draw(self, save=None, show=True):
        """Draw all trees contained in history
        
        :param save: if not None, the file to save figures
        :param show: if True, figures are shown
        :type show: :class:`bool`
        """
        n_steps = len(self.history)
        for i in range(n_steps):
            if save:
                save_i = save + '_i'
            else:
                save_i = None
            tree = self.history[i]
            highlighted_edge = set()
            highlighted_node = set()
            if i != 0:
                highlighted_node = [self.order[i-1][0].union(self.order[i-1][1])]
            if i != n_steps - 1:
                highlighted_edge = [self.order[i]]
            tree.draw(highlighted_edge=highlighted_edge, highlighted_node=highlighted_node, save=save_i, show=show)

