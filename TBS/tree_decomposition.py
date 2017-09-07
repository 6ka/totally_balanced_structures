from TBS.graph.binary_mixed_tree import BinaryMixedTree
from TBS.graph.mixed_graph import MixedGraph
import random

from TBS.lattice import Lattice


class DecompositionBTB:
    def __init__(self, initial_tree):
        self.tree = BinaryMixedTree(initial_tree)

        self.history = []
        self.lattice = Lattice()
        for x in self.tree.vertices:
            self.lattice.update((("BOTTOM", str(x)),))
        self.store()

    @classmethod
    def init_from_graph(cls, initial_tree):
        decomposition = DecompositionBTB({})
        decomposition.tree = BinaryMixedTree.from_tree(initial_tree)
        return decomposition

    def store(self):
        self.history.append(MixedGraph(self.tree))

    def algo(self):
        while len(self.tree) > 1:
            x, y = self.tree.get_edge()
            self.step(x, y)
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
            else:
                self.tree.move_undirected_from_to(u, xy, self.random_choice(u))

            if len(self.tree.undirected[u]) == 0:
                self.tree.remove_vertex(u)

    def random_choice(self, u):
        population = list(self.tree.undirected[u])
        random.shuffle(population)
        k = random.randint(0, len(population))

        return population[:k]

    def algo_from_lattice(self, lattice, order=None):
        if not order:
            order = iter(lattice.contraction_order())
        already_created = set()
        for vertex in order:
            self.contract_tree_edge_from_lattice(vertex, already_created, lattice)
            self.store()

    def contract_tree_edge_from_lattice(self, class_to_create, already_created, lattice):
        clusters = lattice.sup_irreducible_clusters()
        lattice_index_correspondance = {clusters[x]: x for x in clusters}
        dual = lattice.dual_lattice
        already_created.add(class_to_create)
        pred1, pred2 = clusters[dual[class_to_create][0]], clusters[dual[class_to_create][1]]
        self.tree.remove_undirected(pred1, pred2)
        self.tree.add_vertex(clusters[class_to_create])
        for predecessor in dual[class_to_create]:
            if len(lattice[predecessor]) == 1:
                self.tree.move_undirected_from_to(clusters[predecessor], clusters[class_to_create])
                for directed_neighbour in self.tree.directed[clusters[predecessor]]:
                    self.tree.add_undirected(directed_neighbour, clusters[class_to_create])
                self.tree.remove_vertex(clusters[predecessor])
            elif len(lattice[predecessor]) == 2:
                if lattice[predecessor][0] == class_to_create:
                    other_succ = lattice[predecessor][1]
                elif lattice[predecessor][1] == class_to_create:
                    other_succ = lattice[predecessor][0]
                else:
                    raise ValueError("Lattice is not binary")
                if other_succ not in already_created:
                    self.tree.add_directed(clusters[predecessor], clusters[class_to_create])
                    neighbours_at_beginning = self.tree.undirected[clusters[predecessor]].copy()
                    for undirected_neighbour in neighbours_at_beginning:
                        if lattice.sup_filter(lattice_index_correspondance[undirected_neighbour]).intersection(
                                        lattice.sup_filter(predecessor)) <= lattice.sup_filter(class_to_create):
                            self.tree.remove_undirected(undirected_neighbour, clusters[predecessor])
                            self.tree.add_undirected(undirected_neighbour, clusters[class_to_create])
                else:
                    self.tree.move_undirected_from_to(clusters[predecessor], clusters[class_to_create])
                    self.tree.add_undirected(clusters[other_succ], clusters[class_to_create])
                    self.tree.remove_vertex(clusters[predecessor])
            else:
                raise ValueError("Lattice is not binary")
