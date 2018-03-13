__author__ = "cchatel", "fbrucker"

import random

from ._dismantlable_lattice import DismantlableLattice
from ..graph import DirectedGraph


def random_dismantlable_lattice(n_vertices, top="TOP", bottom="BOTTOM", new_vertex=lambda lattice: len(lattice)):
    """Create a random dimantlable lattice.

    Iteratively add a doubly irreducible element to an original 2-element lattice.

    Args:
        n_vertices(int): the number of vertices (excluding bottom and top)
        top: the top element
        bottom: the bottom element
        new_vertex(lattice -> element): a new element.

    Returns(DismantlableLattice): a random dismantlable lattice.
    """

    crown_free = DismantlableLattice(DirectedGraph([bottom, top], [(bottom, top)]))

    all_elements = [bottom]
    for step in range(n_vertices):
        element = new_vertex(crown_free)

        u = random.sample(all_elements, 1)[0]
        v = random.sample(crown_free.above(u) - {u}, 1)[0]
        crown_free.add_join_irreducible(element, u, v)

    return crown_free


def from_dlo_matrix(matrix, bottom="BOTTOM", top="TOP"):
    """ Lattice.

    Vertices are the boxes

    :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
    :param bottom: bottom element
    :param top: top element
    :return: :class:`Graph` associated lattice.
    """

    box_lattice = DirectedGraph()

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

        last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in
                         zip(current_line, last_clusters)]

    for vertex in set(x for x in box_lattice if box_lattice.degree(x) == 0):
        box_lattice.update([(vertex, top)])

    return box_lattice
