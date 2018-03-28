from ..graph import Graph

from ..graph._mixed_graph import MixedGraph, UNDIRECTED_EDGE, DIRECTED_EDGE

from matplotlib import pyplot
import matplotlib

import random
import math


class BinaryMixedTree(MixedGraph):
    def __init__(self, tree):
        super().__init__()
        for vertex in tree:
            self.add(frozenset({vertex}))
        for vertex in tree:
            for neighbour in tree(vertex):
                self.update(UNDIRECTED_EDGE, [(frozenset({vertex}), frozenset({neighbour}))])

    def copy(self):
        copy = BinaryMixedTree({})
        for vertex in self.vertices:
            copy.add(vertex)

        undirected, directed = self.edges
        copy.update(UNDIRECTED_EDGE, undirected)
        copy.update(DIRECTED_EDGE, directed)
        return copy

    def add_undirected(self, x, y):
        self.update(UNDIRECTED_EDGE, [(x, y)])

    def add_directed(self, x, y):
        self.update(DIRECTED_EDGE, [(x, y)])

    def remove_undirected(self, x, y):
        self.difference([(x, y)])

    def remove_directed(self, x, y):
        self.difference([(x, y)])

    def get_edge(self):
        return list(self.edges[0])[0]

    def add_union(self, x, y):
        xy = x.union(y)

        self.difference([(x, y)])
        self.add(xy)

        self.update(DIRECTED_EDGE, [(x, xy), (y, xy)])

        return xy

    def get_other_successor_or_none(self, x, successor):
        if len(self(x, undirected=False, begin=True, end=False)) < 2:
            return None
        else:
            other, s2 = self(x, undirected=False, begin=True, end=False)
            if other == successor:
                other = s2
            return other

    def move_undirected_from_to(self, x, y, edges=None):
        if edges is None:
            edges = set(self(x, undirected=True, begin=False, end=False))

        for z in edges:
            self.difference([(x, z)])
            self.update(UNDIRECTED_EDGE, [(y, z)])

    def move_directed_from_to(self, x, y, edges=None):
        if edges is None:
            edges = set(self(x, undirected=False, begin=False, end=True))

        for z in edges:
            self.difference([(z, x)])
            self.update(DIRECTED_EDGE, [(z, y)])

    def to_graph(self):
        tree = Graph(self.vertices,
                     ((vertex, neighbour) for vertex in self
                      for neighbour in self(vertex, undirected=True, begin=True, end=True)))
        return tree

    def find_root_as_undirected(self):

        pruned_tree = self.to_graph()

        while len(pruned_tree) > 2:
            leaves = [vertex for vertex in pruned_tree if len(pruned_tree(vertex)) == 1]
            for leaf in leaves:
                pruned_tree.remove(leaf)
        possible_roots = [root for root in pruned_tree]  # 1 or 2 possibilities
        return random.choice(possible_roots)
