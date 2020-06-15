import unittest
from unittest.mock import patch

from tbs.lehelian import random_lehelian_hypergraph
from tbs.graph import Graph


class TestInit(unittest.TestCase):

    def test_one_vertex(self):
        self.assertEqual(random_lehelian_hypergraph((1,)), frozenset((frozenset((1,)),)))

    def test_one_edge(self):
        self.assertEqual(random_lehelian_hypergraph((1, 2)), frozenset((frozenset((1,)), frozenset((2,)), frozenset((1, 2)))))

    @patch('tbs.lehelian._creation.random_tree')
    def test_path(self, mocked_random_tree):
        mocked_random_tree.side_effect = lambda vertices: Graph().update([(vertices[i - 1], vertices[i])
                                                                          for i in range(1, len(vertices))])
        self.assertEqual(random_lehelian_hypergraph([1, 2, 3, 4]),
                         frozenset({frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}),
                                    frozenset({1, 2}), frozenset({2, 3}), frozenset({3, 4}),
                                    frozenset({1, 2, 3}), frozenset({2, 3, 4}),
                                    frozenset({1, 2, 3, 4}),
                                    })
                         )

    def test_number_clusters(self):
        self.assertEqual(len(random_lehelian_hypergraph(list(range(10)))), 11 * 10 / 2)
