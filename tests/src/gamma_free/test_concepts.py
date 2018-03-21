import unittest

from tbs.gamma_free.concepts import line_concept_from_dlo_gamma_free_matrix, \
    column_concept_from_dlo_gamma_free_matrix, concepts_from_dlo_gamma_free_matrix


class TestConcepts(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]

    def test_line_concepts(self):
        line_concepts = line_concept_from_dlo_gamma_free_matrix(self.matrix)
        self.assertEqual({(0, 0), (2, 2), (2, 1), (2, 0)},
                         line_concepts)

    def test_column_concepts(self):
        column_concepts = column_concept_from_dlo_gamma_free_matrix(self.matrix)
        self.assertEqual({(0, 0), (1, 0), (2, 0)},
                         column_concepts)

    def test_trace_from_context_matrix(self):
        self.assertEqual(concepts_from_dlo_gamma_free_matrix(self.matrix),
                         {(0, 0), (2, 0)})