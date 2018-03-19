import unittest

from tbs.graph import Graph, mst_from_set, connected_parts


class TestConnectedParts(unittest.TestCase):
    def test_mst(self):
        self.assertEqual(Graph.from_edges([(1, 2), (1, 3)]), mst_from_set([1, 2, 3], lambda x, y: x + y))

    def test_connected_parts(self):
        self.assertEqual(frozenset([frozenset([1, 2, 3])]), connected_parts(Graph.from_edges([(1, 2), (1, 3)])))

    def test_connected_parts_forbidden(self):
        self.assertEqual(frozenset([frozenset([1]), frozenset([3])]),
                         connected_parts(Graph.from_edges([(1, 2), (2, 3)]), [1, 3]))
