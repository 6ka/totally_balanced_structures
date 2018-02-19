from ._mixed_graph import MixedGraph, UNDIRECTED_EDGE, DIRECTED_EDGE

from matplotlib import pyplot
import matplotlib
from ._graph import Graph
import random
import math


class BinaryMixedTree(MixedGraph):
    def __init__(self, tree):
        super().__init__()
        for vertex in tree:
            self.add(frozenset({vertex}))
        for vertex in tree:
            for neighbour in tree[vertex]:
                self.update([(frozenset({vertex}), frozenset({neighbour}))], UNDIRECTED_EDGE)

    def copy(self):
        copy = BinaryMixedTree({})
        for vertex in self.vertices:
            copy.add(vertex)

        undirected, directed = self.edges
        copy.update(undirected, UNDIRECTED_EDGE)
        copy.update(directed, DIRECTED_EDGE)
        return copy

    def add_undirected(self, x, y):
        self.update([(x, y)], UNDIRECTED_EDGE)

    def add_directed(self, x, y):
        self.update([(x, y)], DIRECTED_EDGE)

    def remove_undirected(self, x, y):
        self.update([(x, y)], UNDIRECTED_EDGE, delete=True)

    def remove_directed(self, x, y):
        self.update([(x, y)], DIRECTED_EDGE, delete=True)

    def get_edge(self):
        return list(self.edges[0])[0]

    def add_union(self, x, y):
        xy = x.union(y)

        self.update([(x, y)], UNDIRECTED_EDGE, delete=True)
        self.add(xy)

        self.update([(x, xy), (y, xy)], DIRECTED_EDGE)

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
            self.update([(x, z), (y, z)], UNDIRECTED_EDGE, delete=True)

    def move_directed_from_to(self, x, y, edges=None):
        if edges is None:
            edges = set(self(x, undirected=False, begin=False, end=True))

        for z in edges:
            self.update([(z, x), (z, y)], DIRECTED_EDGE, delete=True)

    def to_graph(self):
        tree = Graph(directed=False)
        for vertex in self.vertices:
            if vertex not in tree:
                tree.add(vertex)
            for neighbour in self(vertex, undirected=False, begin=True, end=False):
                if not tree.isa_edge(neighbour, vertex):
                    tree.update(((vertex, neighbour),))
            for neighbour in self(vertex, undirected=True, begin=False, end=False):
                if not tree.isa_edge(neighbour, vertex):
                    tree.update(((vertex, neighbour),))
        return tree

    def find_root_as_undirected(self):

        pruned_tree = self.to_graph()

        while len(pruned_tree) > 2:
            leaves = [vertex for vertex in pruned_tree if pruned_tree.isa_leaf(vertex)]
            for leaf in leaves:
                pruned_tree.remove(leaf)
        possible_roots = [root for root in pruned_tree]  # 1 or 2 possibilities
        return random.choice(possible_roots)

    def get_radial_tree_coordinates(self, root=None, order=None):
        tree = self.to_graph()
        if len(tree) == 1:
            return {list(tree)[0]: [0, 0]}
        if not root:
            root = self.find_root_as_undirected()
        if not order:
            order = list(tree.topological_sort(root))
        angles = {}
        leaves = [vertex for vertex in order if tree.isa_leaf(vertex) and vertex != root]
        for index, leaf in enumerate(leaves):
            angles[leaf] = 2 * math.pi * index / len(leaves)
        for vertex in reversed(order):
            if vertex not in angles:
                neighbors_angles = [angles[neighbor] for neighbor in tree[vertex] if neighbor in angles]
                angles[vertex] = sum(neighbors_angles) / len(neighbors_angles)
        coordinates = {order[0]: [0, 0]}
        for vertex in order[1:]:
            i = 0
            predecessor = tree[vertex][i]
            while predecessor not in coordinates:
                predecessor = tree[vertex][i + 1]
                i += 1
            coordinates[vertex] = [coordinates[predecessor][0] + math.cos(angles[vertex]),
                                   coordinates[predecessor][1] + math.sin(angles[vertex])]
        return coordinates

    def draw(self, highlighted_edge=set(), highlighted_node=set(), save=None, show=True):
        fig, ax = pyplot.subplots()
        root = self.find_root_as_undirected()
        coordinates = self.get_radial_tree_coordinates(root)
        lines = []
        red_lines = []
        green_lines = []
        for vertex in self.vertices:
            for neighbour in self(vertex, undirected=True, begin=False, end=False):
                if (vertex, neighbour) not in highlighted_edge and (neighbour, vertex) not in highlighted_edge:
                    lines.append([tuple(coordinates[vertex]), tuple(coordinates[neighbour])])
                else:
                    green_lines.append([tuple(coordinates[vertex]), tuple(coordinates[neighbour])])
            for neighbour in self(vertex, undirected=False, begin=True, end=False):
                red_lines.append((coordinates[vertex], coordinates[neighbour]))
        line_collection = matplotlib.collections.LineCollection(lines)
        red_line_collection = matplotlib.collections.LineCollection(red_lines, colors="red")
        green_line_collection = matplotlib.collections.LineCollection(green_lines, colors="#42c432")
        ax.add_collection(line_collection)
        ax.add_collection(red_line_collection)
        ax.add_collection(green_line_collection)
        pyplot.scatter([coordinates[vertex][0] for vertex in coordinates if vertex not in highlighted_node],
                       [coordinates[vertex][1] for vertex in coordinates if vertex not in highlighted_node])
        pyplot.scatter([coordinates[vertex][0] for vertex in highlighted_node],
                       [coordinates[vertex][1] for vertex in highlighted_node], c='#42c432')
        for i, vertex in enumerate(coordinates):
            pyplot.annotate(vertex, (coordinates[vertex][0], coordinates[vertex][1]))
        if save:
            pyplot.savefig(save)
        if show:
            pyplot.show()
        pyplot.close()