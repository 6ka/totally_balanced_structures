__author__ = 'fbrucker'

__all__ = ["from_diss_as_list_of_sets", "from_diss", "from_diss_approximate_order", "is_compatible_for_diss"]


class ClusterOrder:
    def __init__(self, diss):
        self.diss = diss
        self.delta = self._init_non_hierarchical_triplets()
        self.cluster_order = []

    def next_0(self):
        next_in_order = set()

        for x, value in self.delta.items():
            if value == 0:
                next_in_order.add(x)
        return next_in_order

    def next_min(self):
        min_number = None
        min_element = None
        for x, value in self.delta.items():
            if min_number is None or min_number >value:
                min_number = value
                min_element = x
        return {min_element}

    def exact_decomposition(self):
        return self.run(self.next_0)

    def min_decomposition(self):
        return self.run(self.next_min)

    def run(self, next_elements=next_0):
        while self.delta:
            next_in_order = next_elements()

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

    def isa_order(self, possible_order):
        for x in possible_order:
            if self.delta[x] != 0:
                return False
            self.cluster_order.append(x)
            self._update_delta(x)
        return True


def from_diss_as_list_of_sets(diss):
    return ClusterOrder(diss).exact_decomposition().cluster_order


def from_diss_approximate_order(diss):
    return ClusterOrder(diss).min_decomposition().cluster_order


def from_diss(diss):
    list_of_sets = from_diss_as_list_of_sets(diss)
    one_cluster_order = []
    for equivalent_object in list_of_sets:
        one_cluster_order.extend(equivalent_object)
    return one_cluster_order


def is_compatible_for_diss(possible_order, diss):
    return ClusterOrder(diss).isa_order(possible_order)
