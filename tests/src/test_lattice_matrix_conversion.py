__author__ = 'fbrucker'

import unittest

from DLC.graph import Graph
from DLC.contextmatrix import ContextMatrix
from DLC.clusters import cluster_matrix_from_O1_matrix, atom_clusters_correspondence, \
    cover_graph_from_matrix
from DLC.lattice import sup_irreducible_clusters, get_bottom, get_top
from DLC.randomize import random_dismantable_lattice


class TestLatticeMatrixConversion(unittest.TestCase):
    def setUp(self):
        self.lattice = Graph(directed=True).update([(1, 2),
                                                    (2, "TOP"),
                                                    (3, 1),
                                                    (4, "TOP"),
                                                    (5, 2),
                                                    (5, 4),
                                                    (6, 3),
                                                    (6, 7),
                                                    (7, "TOP"),
                                                    (8, 5),
                                                    (8, 7),
                                                    ("BOTTOM", 8),
                                                    ("BOTTOM", 6)])

    def test_conversion(self):
        context_matrix = ContextMatrix.from_cover_graph(self.lattice)
        context_matrix.reorder_doubly_lexical_order()
        clusters = cluster_matrix_from_O1_matrix(context_matrix.matrix)
        number_to_cluster, cluster_to_number = atom_clusters_correspondence(clusters, context_matrix.elements)

        number_to_cluster_lattice = sup_irreducible_clusters(self.lattice)
        self.assertEqual(set(cluster_to_number).union([frozenset(), frozenset(context_matrix.elements)]),
                         set(number_to_cluster_lattice.values()))

    def test_lattice(self):
        context_matrix = ContextMatrix.from_cover_graph(self.lattice)
        context_matrix.reorder_doubly_lexical_order()
        clusters = cluster_matrix_from_O1_matrix(context_matrix.matrix)
        number_to_cluster, cluster_to_number = atom_clusters_correspondence(clusters, context_matrix.elements)
        number_to_cluster_lattice = sup_irreducible_clusters(self.lattice)

        matrix_lattice = cover_graph_from_matrix(context_matrix.matrix, bottom=get_bottom(self.lattice),
                                                 top=get_top(self.lattice))
        for number, cluster in number_to_cluster.items():
            matrix_lattice.rename(number, cluster)

        for number, cluster in number_to_cluster_lattice.items():
            if cluster in matrix_lattice:
                matrix_lattice.rename(cluster, number)

        self.assertEqual(self.lattice, matrix_lattice)

    def test_random_lattices(self):
        for i in range(10):
            lattice = random_dismantable_lattice(30)
            context_matrix = ContextMatrix.from_cover_graph(lattice)
            context_matrix.reorder_doubly_lexical_order()
            clusters = cluster_matrix_from_O1_matrix(context_matrix.matrix)
            number_to_cluster, cluster_to_number = atom_clusters_correspondence(clusters, context_matrix.elements)
            number_to_cluster_lattice = sup_irreducible_clusters(lattice)

            matrix_lattice = cover_graph_from_matrix(context_matrix.matrix, bottom=get_bottom(lattice),
                                                     top=get_top(lattice))
            for number, cluster in number_to_cluster.items():
                matrix_lattice.rename(number, cluster)

            for number, cluster in number_to_cluster_lattice.items():
                if cluster in matrix_lattice:
                    matrix_lattice.rename(cluster, number)

            # should (hopefully) not happen
            if lattice != matrix_lattice:
                from graphics.lattice_string import from_context_matrix
                print("The random test failed")
                print("The matrix:")
                print(from_context_matrix(context_matrix))
                print("the original graph:")
                print(lattice)
            self.assertEqual(lattice, matrix_lattice)

