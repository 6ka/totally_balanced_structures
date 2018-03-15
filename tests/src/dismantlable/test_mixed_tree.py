import unittest

from tbs.graph import Graph
from tbs.dismantlable import BinaryMixedTree


class TestMixedTree(unittest.TestCase):
    def test_two_vertices(self):
        tree = BinaryMixedTree(Graph([0, 1], [(0, 1)]))
        zero = frozenset([0])
        one = frozenset([1])

        self.assertEqual(2, len(tree))
        self.assertEqual({zero, one}, tree.vertices)
        self.assertEqual([frozenset([frozenset([zero, one])]), frozenset()], tree.edges)

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
        mixed = BinaryMixedTree(Graph.from_neighborhoods(tree))

        mixed.remove_undirected(frozenset([3]), frozenset([9]))
        mixed.add_directed(frozenset([3]), frozenset([9]))

        mixed.move_undirected_from_to(frozenset([3]), frozenset([9]))

        self.assertEqual(0, len(mixed(frozenset([3]), undirected=True, begin=False, end=False)))
        self.assertEqual({frozenset([9])}, mixed(frozenset([3]), undirected=False, begin=True, end=False))
        self.assertEqual(set(frozenset([x]) for x in [0, 1, 4, 5, 6, 8]),
                         mixed(frozenset([9]), undirected=True, begin=False, end=False))

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
        mixed = BinaryMixedTree(Graph.from_neighborhoods(tree))

        mixed.remove_undirected(frozenset([3]), frozenset([9]))
        mixed.add_directed(frozenset([3]), frozenset([9]))

        mixed.move_undirected_from_to(frozenset([3]), frozenset([9]), set(frozenset([x]) for x in [1, 4, 8]))

        self.assertEqual({frozenset([9])}, mixed(frozenset([3]), undirected=False, begin=True, end=False))
        self.assertEqual(set(frozenset([x]) for x in [5, 6]),
                         mixed(frozenset([3]), undirected=True, begin=False, end=False))
        self.assertEqual(set(frozenset([x]) for x in [0, 1, 4, 8]),
                         mixed(frozenset([9]), undirected=True, begin=False, end=False))

    def test_move_directed_edges_all(self):
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
        mixed = BinaryMixedTree(Graph.from_neighborhoods(tree))

        mixed.remove_undirected(frozenset([3]), frozenset([1]))
        mixed.remove_undirected(frozenset([3]), frozenset([4]))
        mixed.add_directed(frozenset([1]), frozenset([3]))
        mixed.add_directed(frozenset([4]), frozenset([3]))

        mixed.move_directed_from_to(frozenset([3]), frozenset([9]))

        self.assertEqual(0, len(mixed(frozenset([3]), undirected=False, begin=False, end=True)))
        self.assertEqual({frozenset([1]), frozenset([4])},
                         mixed(frozenset([9]), undirected=False, begin=False, end=True))
        self.assertEqual(set(frozenset([x]) for x in [5, 6, 8, 9]),
                         mixed(frozenset([3]), undirected=True, begin=False, end=False))

    def test_move_directed_edges_some(self):
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
        mixed = BinaryMixedTree(Graph.from_neighborhoods(tree))

        mixed.remove_undirected(frozenset([3]), frozenset([1]))
        mixed.remove_undirected(frozenset([3]), frozenset([4]))
        mixed.add_directed(frozenset([1]), frozenset([3]))
        mixed.add_directed(frozenset([4]), frozenset([3]))

        mixed.move_directed_from_to(frozenset([3]), frozenset([9]), [frozenset([1])])

        self.assertEqual({frozenset([1])}, mixed(frozenset([9]), undirected=False, begin=False, end=True))
        self.assertEqual({frozenset([4])}, mixed(frozenset([3]), undirected=False, begin=False, end=True))
        self.assertEqual(set(frozenset([x]) for x in [5, 6, 8, 9]),
                         mixed(frozenset([3]), undirected=True, begin=False, end=False))

    def test_to_graph(self):
        mixed = BinaryMixedTree({})
        for i in range(7):
            mixed.add(i)
        mixed.add_directed(3, 6)
        mixed.add_directed(2, 5)
        mixed.add_undirected(0, 1)
        mixed.add_undirected(0, 2)
        mixed.add_undirected(0, 3)
        mixed.add_undirected(1, 4)
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5, 6], edges=((0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)))
        self.assertEqual(tree, mixed.to_graph())

    def test_find_root(self):
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5, 6], edges=((0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)))
        binary_mixed_tree = BinaryMixedTree(tree)
        root = binary_mixed_tree.find_root_as_undirected()
        self.assertEqual(root, frozenset({0}))
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5], edges=((0, 1), (0, 2), (0, 3), (1, 4), (1, 5)))
        binary_mixed_tree = BinaryMixedTree(tree)
        root = binary_mixed_tree.find_root_as_undirected()
        self.assertTrue(root == frozenset({0}) or root == frozenset({1}))
