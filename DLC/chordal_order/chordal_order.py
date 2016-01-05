__author__ = 'fbrucker'

__all__ = ["from_diss_as_list_of_sets", "from_diss"]


class ClusterOrder:
    def __init__(self, diss):
        self.diss = diss
        self.delta = self._init_non_hierarchical_triplets()
        self.cluster_order = []

    def run(self):
        while self.delta:
            next_in_order = set()

            for x, value in self.delta.items():
                if value == 0:
                    next_in_order.add(x)

            if not next_in_order:
                return self
            else:
                for x in next_in_order:
                    self._update_delta(x)
                self.cluster_order.append(next_in_order)

        return self

    def _init_non_hierarchical_triplets(self):
        diss = self.diss

        delta = dict()
        for x in diss:
            delta[x] = 0
            for y in diss:
                for z in diss:
                    if diss(y, z) > max(diss(x, y), diss(x, z)):
                        delta[x] += 1
        return delta

    def _update_delta(self, z):
        del self.delta[z]
        for x in self.delta:
            for y in self.delta:
                if self.diss(y, z) > max(self.diss(x, y), self.diss(x, z)):
                    self.delta[x] -= 2 * 1


def from_diss_as_list_of_sets(diss):
    return ClusterOrder(diss).run().cluster_order


def from_diss(diss):
    list_of_sets = from_diss_as_list_of_sets(diss)
    one_cluster_order = []
    for equivalent_object in list_of_sets:
        one_cluster_order.extend(equivalent_object)
    return one_cluster_order
