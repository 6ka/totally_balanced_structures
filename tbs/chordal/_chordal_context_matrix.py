from ..contextmatrix import ContextMatrix
from ._chordal_order import chordal_order


__all__ = ["chordal_context_matrix"]


def chordal_context_matrix(d, order=None):
    """ Context Matrix of a chordal dissimilarity.

    Args:
        d(Diss): chordal dissimilarity
        order(list): If None an order is first searched, must be a chordal order (thus also d) otherwise.

    The line are ordered by a chordal order (parameter order if given) and the columns by inclusion following
    the reverse order.

    Returns(ContextMatrix: The cluster context matrix whole lines are ordered by a chordal order.

    """

    if order is None:
        order = chordal_order(d)

    clusters = chordal_clusters(d, order)
    columns_clusters = []
    for order_clusters in reversed(sort_clusters_by_order(clusters, order)):
        columns_clusters.extend(order_clusters)

    return ContextMatrix.from_clusters(columns_clusters, order)


def chordal_clusters(d, order=None):
    """ Clusters of a chordal dissimilarity.

    Args:
        d (Diss): a chordal dissimilarity
        order (list): If None an order is first searched, must be a chordal order otherwise.

    Returns: A set of clusters

    """

    if order is None:
        order = chordal_order(d)

    def d_order(x, y):
        return d(order[x], order[y])

    clusters = set()
    cluster_diameter_for_sizes = [[-1] * (len(d) + 1)]

    for j in range(len(d)):
        ball_0_j = frozenset(order[i] for i in range(len(d)) if d_order(0, i) <= d_order(0, j))
        clusters.add(ball_0_j)
        cluster_diameter_for_sizes[0][len(ball_0_j) - 1] = d_order(0, j)  # -1 because 0 is removed from the elements.

    for i in range(1, len(d)):
        cluster_diameter_for_sizes.append([-1] * (len(d) + 1))

        for j in range(i, len(d)):
            c_ij = frozenset(order[k] for k in range(i, len(d)) if d_order(i, k) <= d_order(i, j))

            is_a_cluster = True
            for k in range(i):
                if d_order(k, i) <= d_order(i, j) and cluster_diameter_for_sizes[k][len(c_ij)] == d_order(i, j):
                    is_a_cluster = False
                    break

            if is_a_cluster:
                clusters.add(c_ij)
                cluster_diameter_for_sizes[i][len(c_ij) - 1] = d_order(i, j)

        for j in range(i):
            for k in range(1, len(d) + 1):
                if cluster_diameter_for_sizes[j][k] >= d_order(j, i):
                    if k > 1 and cluster_diameter_for_sizes[j][k - 1] == -1:
                        cluster_diameter_for_sizes[j][k - 1] = cluster_diameter_for_sizes[j][k]
                    cluster_diameter_for_sizes[j][k] = -1

    return clusters


def sort_clusters_by_order(clusters, order):
    clusters_by_length = list(clusters)
    clusters_by_length.sort(key=lambda x: len(x))

    clusters_by_order = [[] for x in order]
    for cluster in clusters_by_length:
        for i, x in enumerate(order):
            if x in cluster:
                clusters_by_order[i].append(cluster)
                break
    return clusters_by_order
