from TBS.tree import random_tree
from TBS.graph.binary_mixed_tree import BinaryMixedTree
import unittest


class TestMixedTree(unittest.TestCase):
    def test_two_vertices_random_tree(self):
        tree = random_tree(2)
        zero = 0
        one = 1
        self.assertEqual(2,
                         len(tree))

        self.assertEqual({zero: {one},
                          one: {zero},
                          },
                         tree)

    def test_two_vertices(self):
        tree = BinaryMixedTree(random_tree(2))
        zero = frozenset([0])
        one = frozenset([1])

        self.assertEqual(2,
                         len(tree))

        self.assertEqual({zero: {one},
                          one: {zero},
                          },
                         tree.undirected)

        self.assertEqual({zero: set(),
                          one: set(),
                          },
                         tree.directed)
        self.assertEqual({zero: set(),
                          one: set(),
                          },
                         tree.directed_dual)

    def test_move_edges_all(self):
        tree = {7: [5],
                5: [7, 2, 3],
                3: [5, 6, 8, 4, 1, 9],
                0: [9],
                6: [3],
                8: [3],
                4: [3],
                1: [3],
                2: [5],
                9: [3, 0]
                }
        mixed = BinaryMixedTree(tree)

        mixed.remove_undirected(frozenset([3]), frozenset([9]))
        mixed.add_directed(frozenset([3]), frozenset([9]))

        mixed.move_undirected_from_to(frozenset([3]), frozenset([9]))

        self.assertEqual(0, len(mixed.undirected[frozenset([3])]))
        self.assertEqual({frozenset([9])}, mixed.directed[frozenset([3])])
        self.assertEqual(set(frozenset([x]) for x in [0, 1, 4, 5, 6, 8]), mixed.undirected[frozenset([9])])

    def test_move_edges_some(self):
        tree = {7: [5],
                5: [7, 2, 3],
                3: [5, 6, 8, 4, 1, 9],
                0: [9],
                6: [3],
                8: [3],
                4: [3],
                1: [3],
                2: [5],
                9: [3, 0]
                }
        mixed = BinaryMixedTree(tree)

        mixed.remove_undirected(frozenset([3]), frozenset([9]))
        mixed.add_directed(frozenset([3]), frozenset([9]))

        mixed.move_undirected_from_to(frozenset([3]), frozenset([9]), set(frozenset([x]) for x in [1, 4, 8]))

        self.assertEqual({frozenset([9])}, mixed.directed[frozenset([3])])
        self.assertEqual(set(frozenset([x]) for x in [5, 6]), mixed.undirected[frozenset([3])])
        self.assertEqual(set(frozenset([x]) for x in [0, 1, 4, 8]), mixed.undirected[frozenset([9])])