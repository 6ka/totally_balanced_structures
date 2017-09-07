from TBS.graph.binary_mixed_tree import BinaryMixedTree
from TBS.graph.mixed_graph import MixedGraph
import random


class DecompositionBTB:
    def __init__(self, initial_tree):
        self.tree = BinaryMixedTree(initial_tree)

        self.history = []
        self.clusters = [x for x in self.tree.vertices]
        self.store()

    def store(self):
        self.history.append(MixedGraph(self.tree))

    def algo(self):
        while len(self.tree) > 1:
            x, y = self.tree.get_edge()
            self.step(x, y)
            self.store()
            self.clusters.append(x.union(y))

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