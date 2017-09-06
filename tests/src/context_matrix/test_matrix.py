# -*- coding: utf-8 -*-

import unittest
from TBS.contextmatrix import ContextMatrix
from TBS.lattice import Lattice


class TestMatrixCreate(unittest.TestCase):

    def setUp(self):
        self.matrix = [[1, 0, 0, 1, 0],
                       [1, 1, 1, 1, 1],
                       [0, 1, 0, 1, 0],
                       [0, 0, 1, 0, 1]]

    def test_create_bare(self):

        context_matrix = ContextMatrix(self.matrix)
        self.assertEqual(self.matrix, context_matrix._matrix)
        self.assertEqual((0, 1, 2, 3), context_matrix.elements)
        self.assertEqual((0, 1, 2, 3, 4), context_matrix.attributes)

    def test_create_attributes_and_elements(self):

        context_matrix = ContextMatrix(self.matrix, elements=(1, 2, 3, 4), attributes=(5, 6, 7, 8, 9))
        self.assertEqual(self.matrix, context_matrix._matrix)
        self.assertEqual((1, 2, 3, 4), context_matrix.elements)
        self.assertEqual((5, 6, 7, 8, 9), context_matrix.attributes)


class TestMatrix(unittest.TestCase):

    def setUp(self):
        matrix = [[1, 0, 0, 1, 0],
                  [1, 1, 1, 1, 1],
                  [0, 1, 0, 1, 0],
                  [0, 0, 1, 0, 1]]

        self.context_matrix = ContextMatrix(matrix, elements=(1, 2, 3, 4), attributes=(5, 6, 7, 8, 9))

    def test_matrix(self):

        self.assertEqual(len(self.context_matrix.elements), len(self.context_matrix._matrix))

        check = [(self.context_matrix.elements.index(1), (1, 5, 8)),
                 (self.context_matrix.elements.index(2), (5, 6, 7, 8, 9)),
                 (self.context_matrix.elements.index(3), (3, 6, 8)),
                 (self.context_matrix.elements.index(4), (4, 7, 9))]

        for line, columns in check:
            for index in range(len(self.context_matrix._matrix[line])):
                self.assertEqual(len(self.context_matrix.attributes), len(self.context_matrix._matrix[line]))
                if self.context_matrix.attributes[index] in columns:
                    self.assertEqual(1, self.context_matrix._matrix[line][index])
                else:
                    self.assertEqual(0, self.context_matrix._matrix[line][index])

    def test_transpose(self):
        transpose = self.context_matrix.transpose()
        self.assertEqual(self.context_matrix.elements, transpose.attributes)
        self.assertEqual(self.context_matrix.attributes, transpose.elements)
        self.assertEqual(self.context_matrix._matrix, transpose.transpose().matrix)

    def test_renaming(self):
        self.context_matrix.elements = ["a", "b", "c", "d"]
        self.assertEqual(("a", "b", "c", "d"), self.context_matrix.elements)
        self.context_matrix.attributes = range(len(self.context_matrix.attributes))
        self.assertEqual(tuple(range(len(self.context_matrix.attributes))), self.context_matrix.attributes)

    def test_ordering(self):
        line_new_order = list(range(len(self.context_matrix.elements)))
        line_new_order.reverse()
        self.context_matrix.reorder(line_new_order)
        self.assertEqual(tuple([4, 3, 2, 1]), self.context_matrix.elements)
        self.assertEqual([0, 1, 0, 1, 0], self.context_matrix._matrix[1])
        column_new_order = list(range(len(self.context_matrix.attributes)))
        column_new_order.reverse()
        self.context_matrix.reorder(column_permutation=column_new_order)
        self.assertEqual(tuple([9, 8, 7, 6, 5]), self.context_matrix.attributes)
        self.assertEqual([1, 0, 1, 0, 0], self.context_matrix._matrix[0])

    def test_sub_matrix(self):
        sub_matrix = self.context_matrix.submatrix_elements([2, 3, 1])
        self.assertEqual((1, 2, 3), sub_matrix.elements)
        self.assertEqual(self.context_matrix.attributes, sub_matrix.attributes)


class TestDoublyLexicalOrdering(unittest.TestCase):
    def test_doubly_lexical_ordering(self):
        context_matrix = ContextMatrix([[1, 1], [1, 0]])
        context_matrix.reorder_doubly_lexical_order()
        self.assertEqual([[0, 1], [1, 1]], context_matrix._matrix)
        self.assertEqual((1, 0), context_matrix.elements)
        self.assertEqual((1, 0), context_matrix.attributes)


class TestFromCoverGraph(unittest.TestCase):
    def new_lattice(self):
        lattice = Lattice()
        lattice.update([("bottom", 1),
                        ("bottom", 2),
                        ("bottom", 3),
                        ("bottom", 4),
                        (1, 5),
                        (2, 5),
                        (2, 6),
                        (2, 7),
                        (3, 6),
                        (4, 7),
                        (5, 8),
                        (6, 8),
                        (7, 9),
                        (8, "top"),
                        (9, "top")])
        return lattice

    def setUp(self):
        self.lattice = self.new_lattice()

    def test_inf_sup(self):
        context_matrix = ContextMatrix.from_lattice(self.lattice)

        self.assertEqual(frozenset(context_matrix.attributes), frozenset(self.lattice.inf_irreducible()))
        self.assertEqual(frozenset(context_matrix.elements), frozenset(self.lattice.sup_irreducible()))

    def test_matrix(self):
        context_matrix = ContextMatrix.from_lattice(self.lattice)
        self.assertEqual(len(context_matrix.elements), len(context_matrix.matrix))

        check = [(context_matrix.elements.index(1), (1, 5, 8)),
                 (context_matrix.elements.index(2), (5, 6, 7, 8, 9)),
                 (context_matrix.elements.index(3), (3, 6, 8)),
                 (context_matrix.elements.index(4), (4, 7, 9))]
        for line, columns in check:
            for index in range(len(context_matrix.matrix[line])):
                self.assertEqual(len(context_matrix.attributes), len(context_matrix.matrix[line]))
                if context_matrix.attributes[index] in columns:
                    self.assertEqual(1, context_matrix.matrix[line][index])
                else:
                    self.assertEqual(0, context_matrix.matrix[line][index])


class TestFromClusters(unittest.TestCase):
    def test_from_clusters(self):
        context_matrix = ContextMatrix.from_clusters({frozenset({'z', 'y'}),  frozenset({'x', 'y'})})

        self.assertEqual(set(context_matrix.elements), {'x', 'y', 'z'})

        context_matrix.reorder([{'x': 0, 'y': 1, 'z': 2}[x] for x in context_matrix.elements])
        if context_matrix.matrix[0][0] == 0:
            context_matrix.reorder(column_permutation=[1, 0])

        self.assertEqual([[1, 0],
                          [1, 1],
                          [0, 1]],
                         context_matrix.matrix)
