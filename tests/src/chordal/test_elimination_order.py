import unittest

from tbs.graph import Graph
from tbs.chordal._elimination_order import elimination_order, isa_elimination_order, isa_ultrametric_edge, \
    simple_elimination_order, \
    make_sets, simple_to_strong_elimination_order_partition


class TestChordalGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph.from_edges(((1, 2), (2, 3)))

    def test_ultrametric_edge(self):
        self.assertFalse(isa_ultrametric_edge(self.g, 2, 1, 3))
        self.assertFalse(isa_ultrametric_edge(self.g, 2, 3, 1))

        self.assertTrue(isa_ultrametric_edge(self.g, 1, 2, 3))
        self.assertTrue(isa_ultrametric_edge(self.g, 1, 3, 2))

    def test_chordal_order(self):
        order = elimination_order(self.g)

        self.assertEqual({1, 2, 3}, set(order))
        self.assertNotEqual(2, order[0])

    def test_isa_chordal_order(self):
        self.assertTrue(isa_elimination_order(self.g, (1, 2, 3)))
        self.assertFalse(isa_elimination_order(self.g, (2, 1, 3)))

    def test_simple_elimination_order(self):
        order = simple_elimination_order(self.g)
        self.assertEqual({1, 2, 3}, set(order))
        self.assertNotEqual(2, order[0])


class TestSimpleToStrong(unittest.TestCase):

    def setUp(self):
        self.g = Graph.from_edges((('a', 'f'),
                                   ('b', 'e'), ('b', 'f'), ('b', 'g'),
                                   ('c', 'd'), ('c', 'e'),
                                   ('d', 'e'), ('d', 'f'),
                                   ('e', 'f'), ('e', 'g'),
                                   ('f', 'g')))

    def test_make_sets(self):
        self.assertEqual([{'a'}, {'b', 'g'}, {'c'}, {'d', 'e', 'f'}], make_sets(self.g, "abcdefg"))

    def test_simple_to_strong_elimination_order_partition(self):
        self.assertEqual([{'a'}, {'b', 'g'}, {'c'}, {'f'}, {'d'}, {'e'}],
                         simple_to_strong_elimination_order_partition(self.g, "abcdefg"))
