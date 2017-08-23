from TBS.observer import Observable
from TBS.graph import Graph


class Lattice(Graph, Observable):
    def __init__(self, vertices=tuple(), edges=tuple(), dual=None):
        Observable.__init__(self)
        Graph.__init__(self, directed=True)
        if dual is None:
            self.dual = Lattice(dual=self)
        else:
            self.dual = dual
        self.attach(self.dual)
        self._neighborhood = {}

        for x in vertices:
            self._neighborhood[x] = {}

        if edges:
            self.update(edges)

    def update(self, edges=tuple(), node_creation=True, delete=True):
        Graph.update(self, edges, node_creation=True, delete=True)
        for obs in self.observers:
            obs.dual_update(edges)

    def dual_update(self, edges):
        Graph.update(self, ((y, x) for (x, y) in edges))
