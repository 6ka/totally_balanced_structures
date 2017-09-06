import unittest
from TBS.graph import Graph
from tree import find_root


class TestTree(unittest.TestCase):
    def test_find_root(self):
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5, 6], edges=((0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)))
        root = find_root(tree)
        self.assertEqual(root, 0)
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5], edges=((0, 1), (0, 2), (0, 3), (1, 4), (1, 5)))
        root = find_root(tree)
        self.assertTrue(root == 0 or root == 1)
