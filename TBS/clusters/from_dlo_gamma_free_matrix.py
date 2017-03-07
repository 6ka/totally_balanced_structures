
from ..graph import Graph
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


def lattice(matrix, bottom="BOTTOM", top="TOP"):
    """ Lattice.

    Vertices are the boxes (see :func:`boxes`).

    :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
    :param bottom: bottom element
    :param top: top element
    :return: :class:`Graph` associated lattice.
    """

    box_lattice = Graph(directed=True)

    cluster_correspondence = ClusterLineFromMatrix.boxes(matrix)

    last_line = last_line_not_0_for_matrix(matrix)
    last_clusters = [None] * len(matrix[0])
    line_iterator = ClusterLineFromMatrix(matrix)

    for i, current_line in enumerate(line_iterator):
        for j, elem in enumerate(current_line):
            if elem is None:
                continue

        j = len(current_line) - 1
        while j >= 0:
            if current_line[j] is None or current_line[j] in box_lattice:
                j -= 1
                continue

            current_cluster = current_line[j]
            # connect to bottom
            if i == last_line[j]:
                box_lattice.update([(bottom, cluster_correspondence[current_cluster])])

            # successor in line
            right_successor = True
            j_next = j + 1
            while j_next < len(current_line) and current_line[j_next] is None:
                j_next += 1

            if j_next == len(current_line):
                right_successor = False
            if i > 0 and line_iterator.previous_line[j] is not None:
                if j_next == len(current_line) or current_line[j_next] == line_iterator.previous_line[j_next]:
                    right_successor = False
            if right_successor:
                box_lattice.update([(cluster_correspondence[current_cluster],
                                     cluster_correspondence[current_line[j_next]])])

            # successor before line
            while j >= 0 and current_line[j] == current_cluster:
                if last_clusters[j] is not None and last_clusters[j] != current_cluster:
                    box_lattice.update([(cluster_correspondence[current_cluster],
                                         cluster_correspondence[last_clusters[j]])])
                    successor = last_clusters[j]
                    while j >= 0 and last_clusters[j] == successor:
                        j -= 1
                else:
                    break

            while j >= 0 and current_line[j] == current_cluster:
                j -= 1

        last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in zip(current_line, last_clusters)]

    for vertex in set(x for x in box_lattice if box_lattice.degree(x) == 0):
        box_lattice.update([(vertex, top)])

    return box_lattice


def last_line_not_0_for_matrix(matrix):
    last_line = [-1] * len(matrix[0])
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j] == 1:
                last_line[j] = i
                break
    return last_line
