from TBS.graph.mixed_graph import MixedGraph


class BinaryMixedTree(MixedGraph):
    def __init__(self, tree):
        super().__init__()

        for x in tree:
            self.add_vertex(frozenset([x]))

        for x, neighbor in tree.items():
            for y in neighbor:
                self.add_undirected(frozenset([x]), frozenset([y]))

    @classmethod
    def from_tree(cls, tree):
        mixed_graph = BinaryMixedTree({})
        for vertex in tree:
            mixed_graph.add_vertex(vertex)
        for vertex in tree:
            for neighbour in tree[vertex]:
                mixed_graph.add_undirected(vertex, neighbour)
        return mixed_graph

    def get_edge(self):
        for x, neighbors in self.undirected.items():
            for y in neighbors:
                if not self.directed_dual[x] and not self.directed_dual[y]:
                    return x, y

    def add_union(self, x, y):
        xy = x.union(y)

        self.remove_undirected(x, y)
        self.add_vertex(xy)

        self.add_directed(x, xy)
        self.add_directed(y, xy)

        return xy

    def get_other_successor_or_none(self, x, successor):
        if len(self.directed[x]) < 2:
            return None
        else:
            other, s2 = self.directed[x]
            if other == successor:
                other = s2
            return other

    def move_undirected_from_to(self, x, y, edges=None):
        if edges is None:
            edges = set(self.undirected[x])

        for z in edges:
            self.remove_undirected(x, z)
            self.add_undirected(y, z)