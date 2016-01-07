__author__ = 'fbrucker'


class Balls:
    def __init__(self, diss):
        self.diss = diss

    def __call__(self, center, radius, base_set=None):
        if base_set is None:
            base_set = self.diss
        return frozenset(x for x in base_set if self.diss(center, x) <= radius)


def clusters_from_order(diss, chordal_order):
    clusters = set()
    balls = Balls(diss)
    sizes = [[-1] * (len(diss) + 1)]
    for j in range(len(diss)):
        radius = diss(chordal_order[0], chordal_order[j])
        ball = balls(chordal_order[j], radius)
        sizes[0][len(ball) - 1] = radius
        clusters.add(ball)

    for i in range(1, len(diss)):
        sizes.append([-1] * (len(diss) + 1))
        subset_i = chordal_order[i:]
        for j in range(i, len(diss)):
            radius = diss(chordal_order[i], chordal_order[j])
            possible_cluster_ij = balls(chordal_order[i], radius, subset_i)
            is_a_cluster = True
            for k in range(i):
                if diss(chordal_order[k], chordal_order[i]) <= radius and \
                        sizes[k][len(possible_cluster_ij)] == \
                        radius:
                    is_a_cluster = False
                    break

            if is_a_cluster:
                sizes[i][len(possible_cluster_ij) - 1] = radius
                clusters.add(possible_cluster_ij)
        for j in range(i):
            for k in range(1, len(diss) + 1):
                if sizes[j][k] >= diss(chordal_order[j], chordal_order[i]):
                    if k >= 1 and sizes[j][k - 1] == -1:
                        sizes[j][k - 1] = sizes[j][k]
                    sizes[j][k] = -1

    return clusters
