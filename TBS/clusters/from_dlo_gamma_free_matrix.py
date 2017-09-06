from .ClusterLineFromMatrix import ClusterLineFromMatrix

__author__ = 'fbrucker'

__all__ = ["cluster_matrix", "boxes", "lattice"]


def cluster_matrix(matrix):
    """ Cluster Matrix.

    Return a new matrix with the same dimensions. Each cell is equal to either None (if no box cluster) or
    and integer (label of the cluster).

    Each integer forms a box representing the cluster. See [BP_15_ICFCA]_ for detailed explanations.

    :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
    :return: a matrix with the same dimensions.
    """

    return [current_line for current_line in ClusterLineFromMatrix(matrix)]


def boxes(matrix):
    """ Boxes and cluster number correspondence.

    A box is a couple ((l1, c1), (l2, c2)) where (l1, c1) is the top left corner (line, column) of the box and
    (l2, c2) the bottom right corner.

    :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
    :return: :class:`dict` with key= class number and value= the associated box
    """

    cluster_correspondence = dict()

    for i, line in enumerate(ClusterLineFromMatrix(matrix)):
        for j, elem in enumerate(line):
            if elem is None:
                continue
            if elem not in cluster_correspondence:
                cluster_correspondence[elem] = ((i, j), (i, j))
            else:
                begin, end = cluster_correspondence[elem]
                cluster_correspondence[elem] = (begin, (i, j))

    return cluster_correspondence
