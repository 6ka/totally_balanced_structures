from contextmatrix import ContextMatrix

__author__ = 'fbrucker'

__all__ = ["clusters_and_truncated_balls_from_order", "clusters_from_order", "truncated_balls_from_order",
           "context_matrix_from_order", "truncated_balls_correspondence_from_order"]


class Balls:
    def __init__(self, diss):
        self.diss = diss

    def __call__(self, center, radius, base_set=None):
        if base_set is None:
            base_set = self.diss
        return frozenset(x for x in base_set if self.diss(center, x) <= radius)


def clusters_and_truncated_balls_from_order(diss, chordal_order):
    """

    A truncated ball is a couple (i, radius) associated to the set B(x_i, radius) \cap X_i

    Clusters taken by chordal_order order.

    :param diss:
    :param chordal_order:
    :return: 2 lists.
    """

    clusters = list()
    associated_balls = list()
    balls = Balls(diss)
    sizes = [[-1] * (len(diss) + 1)]
    for j in range(len(diss)):
        radius = diss(chordal_order[0], chordal_order[j])
        ball = balls(chordal_order[0], radius)

        if sizes[0][len(ball) - 1] == -1:
            sizes[0][len(ball) - 1] = radius
            clusters.append(ball)
            associated_balls.append((0, radius))

    for i in range(1, len(diss)):
        sizes.append([-1] * (len(diss) + 1))
        subset_i = chordal_order[i:]
        for j in range(i, len(diss)):
            radius = diss(chordal_order[i], chordal_order[j])
            possible_cluster_ij = balls(chordal_order[i], radius, subset_i)
            is_a_cluster = sizes[i][len(possible_cluster_ij) - 1] == -1

            if is_a_cluster:
                for k in range(i):
                    if diss(chordal_order[k], chordal_order[i]) <= radius and \
                            sizes[k][len(possible_cluster_ij)] == \
                            radius:
                        is_a_cluster = False
                        break

            if is_a_cluster:
                sizes[i][len(possible_cluster_ij) - 1] = radius
                clusters.append(possible_cluster_ij)
                associated_balls.append((i, radius))

        for j in range(i):
            for k in range(1, len(diss) + 1):
                if sizes[j][k] >= diss(chordal_order[j], chordal_order[i]):
                    if k >= 1 and sizes[j][k - 1] == -1:
                        sizes[j][k - 1] = sizes[j][k]
                    sizes[j][k] = -1

    return clusters, associated_balls


def clusters_from_order(diss, chordal_order):
    clusters, balls = clusters_and_truncated_balls_from_order(diss, chordal_order)
    return clusters


def truncated_balls_from_order(diss, chordal_order):
    clusters, balls = clusters_and_truncated_balls_from_order(diss, chordal_order)
    return balls


def context_matrix_from_order(diss, chordal_order):
    clusters = clusters_from_order(diss, chordal_order)
    context_matrix = ContextMatrix.from_clusters(clusters)

    line_permutation = [0] * len(context_matrix.matrix)
    for i, index in enumerate(chordal_order):
        line_permutation[index] = i
    context_matrix.reorder(line_permutation=line_permutation)

    return context_matrix


def truncated_balls_correspondence_from_order(diss, chordal_order):
    """
    cluster[i][j]: radius of the first cluster which is a truncated ball centered in x_i containing x_j

    :param diss:
    :param chordal_order:
    :return:
    """
    clusters, balls = clusters_and_truncated_balls_from_order(diss, chordal_order)
    cluster_matrix = [[None] * len(chordal_order) for i in chordal_order]
    for center_index, radius in balls:
        center = chordal_order[center_index]
        for index in range(center_index, len(chordal_order)):
            element = chordal_order[index]
            if diss(center, element) <= radius and \
                    (cluster_matrix[center_index][index] is None or cluster_matrix[center_index][index] > radius):
                cluster_matrix[center_index][index] = radius

    return cluster_matrix
