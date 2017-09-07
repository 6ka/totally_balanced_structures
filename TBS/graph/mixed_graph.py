class MixedGraph:
    def __init__(self, mixed_graph=None):

        self.vertices = set()
        self.undirected = {}
        self.directed = dict()  # x -> y means y in dict[x]
        self.directed_dual = dict()  # x -> y means x in dict[y]

        if mixed_graph is not None:
            self.init_from_mixed_graph(mixed_graph)

    def init_from_mixed_graph(self, other):
        self.vertices = set(other.vertices)

        self.undirected = {k: set(v) for k, v in other.undirected.items()}
        self.directed = {k: set(v) for k, v in other.directed.items()}
        self.directed_dual = {k: set(v) for k, v in other.directed_dual.items()}

    @classmethod
    def init_from_graph(cls, graph):
        mixed_graph = MixedGraph()
        mixed_graph.vertices = {vertex for vertex in graph}
        mixed_graph.undirected = {vertex: set(graph[vertex]) for vertex in graph}
        return mixed_graph

    def __eq__(self, other):
        return self.vertices == other.vertices and self.undirected == other.undirected and self.directed == other.directed

    def __len__(self):
        return len(self.vertices)

    def add_vertex(self, x):
        self.vertices.add(x)
        self.undirected[x] = set()
        self.directed[x] = set()
        self.directed_dual[x] = set()

    def remove_vertex(self, x):
        self.vertices -= frozenset([x])

        for y in self.undirected[x]:
            self.undirected[y].remove(x)
        del self.undirected[x]

        for y in self.directed[x]:
            self.directed_dual[y].remove(x)
        del self.directed[x]

        for y in self.directed_dual[x]:
            self.directed[y].remove(x)
        del self.directed_dual[x]

    def add_undirected(self, u, v):
        self.undirected[u].add(v)
        self.undirected[v].add(u)

    def remove_undirected(self, x, y):
        self.undirected[x].remove(y)
        self.undirected[y].remove(x)

    def add_directed(self, u, v):
        self.directed[u].add(v)
        self.directed_dual[v].add(u)

    def remove_directed(self, u, v):
        self.directed[u].remove(v)
        self.directed_dual[v].remove(u)
