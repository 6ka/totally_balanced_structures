import unittest

from TBS.graph.binary_mixed_tree import BinaryMixedTree
from TBS.tree_decomposition import DecompositionBTB
from TBS.tree import random_tree
from TBS.lattice import Lattice
from TBS.graph import Graph

class TestDecomposition(unittest.TestCase):
    @staticmethod
    def new_lattice():
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

    def test_init_from_graph(self):
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5, 6], edges=((0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)))
        decomposition = DecompositionBTB.init_from_graph_object(tree)
        self.assertEqual(len(decomposition.history), 1)
        self.assertEqual(decomposition.history[0], BinaryMixedTree.from_graph_object(tree))

    def test_algo(self):
        decomposition = DecompositionBTB(random_tree(10))
        decomposition.algo()
        self.assertTrue(decomposition.lattice.is_binary())
        self.assertTrue(decomposition.lattice.is_a_lattice())

    def test_random_choice(self):
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

        decomposition = DecompositionBTB(tree)
        self.assertTrue(
            set(decomposition.random_choice(frozenset({3}))).issubset({frozenset({element}) for element in tree[3]}))

    def test_remove_directed(self):
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

        decomposition = DecompositionBTB(tree)
        decomposition.tree.remove_undirected(frozenset([3]), frozenset([9]))
        decomposition.tree.add_directed(frozenset([3]), frozenset([9]))

        decomposition.random_choice = lambda u: set()
        decomposition.step(frozenset([3]), frozenset([5]))

        self.assertNotIn(frozenset([3]), decomposition.tree.vertices)
        self.assertIn(frozenset([3, 5]), decomposition.tree.vertices)

        self.assertEqual(0, len(decomposition.tree.directed_dual[frozenset([9])]))

        self.assertEqual(set(frozenset([x]) for x in [1, 4, 6, 8, 9]),
                         decomposition.tree.undirected[frozenset([3, 5])])

    def test_contract_edge_one_disappears(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        tree = {1: [2],
                2: [12, 1, 3, 4],
                3: [2],
                4: [2, 10],
                10: [4],
                12: [2]}
        decomposition = DecompositionBTB(tree)
        decomposition.contract_tree_edge_from_lattice(7, set(), self.lattice)
        # contract_24_tree = self.lattice.contract_tree_edge(tree, 7, set())
        self.assertIn(frozenset({1}), decomposition.tree.undirected[frozenset({2})])
        self.assertIn(frozenset({12}), decomposition.tree.undirected[frozenset({2})])
        self.assertIn(frozenset({3}), decomposition.tree.undirected[frozenset({2})])
        self.assertIn(frozenset({2, 4}), decomposition.tree.undirected[frozenset({10})])
        self.assertNotIn(frozenset({4}), decomposition.tree.vertices)
        self.assertEqual(len(decomposition.tree.vertices), 6)

    def test_contract_edge_both_disappear(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        binary_tree = BinaryMixedTree({})
        binary_tree.add_vertex(frozenset({1, 2, 12}))
        binary_tree.add_vertex(frozenset({3, 2, 12}))
        binary_tree.add_vertex(frozenset({2, 4}))
        binary_tree.add_vertex(frozenset({10}))
        binary_tree.add_undirected(frozenset({1, 2, 12}), frozenset({2, 3, 12}))
        binary_tree.add_undirected(frozenset({3, 2, 12}), frozenset({2, 4}))
        binary_tree.add_undirected(frozenset({2, 4}), frozenset({10}))
        decomposition = DecompositionBTB({})
        decomposition.tree = binary_tree
        decomposition.contract_tree_edge_from_lattice(8, {5, 6, 7, 11}, self.lattice)
        self.assertIn(frozenset({1, 2, 3, 12}), decomposition.tree.undirected[frozenset({2, 4})])
        self.assertIn(frozenset({10}), decomposition.tree.undirected[frozenset({2, 4})])
        self.assertNotIn(frozenset({1, 2, 12}), decomposition.tree.vertices)
        self.assertNotIn(frozenset({2, 3, 12}), decomposition.tree.vertices)
        self.assertTrue(len(decomposition.tree.vertices) == 3)

    def test_contract_edge_both_stay(self):
        self.lattice.update(((2, 7), ('bottom', 10), (10, 9), (3, 7)))
        tree = {1: [2],
                2: [1, 3],
                3: [2, 4, 10],
                4: [3],
                10: [3]}
        decomposition = DecompositionBTB(tree)
        decomposition.contract_tree_edge_from_lattice(6, set(), self.lattice)
        self.assertIn(frozenset({1}), decomposition.tree.undirected[frozenset({2})])
        self.assertIn(frozenset({2, 3}), decomposition.tree.directed[frozenset({2})])
        self.assertIn(frozenset({2, 3}), decomposition.tree.directed[frozenset({3})])
        self.assertIn(frozenset({3}), decomposition.tree.undirected[frozenset({10})])
        self.assertIn(frozenset({3}), decomposition.tree.undirected[frozenset({4})])
        self.assertNotIn(frozenset({2}), decomposition.tree.undirected[frozenset({3})])

    def test_contract_edge_one_already_used(self):
        self.lattice.update(((2, 7), ('bottom', 10), (10, 9), (3, 7)))
        binary_tree = BinaryMixedTree({})
        binary_tree.add_vertex(frozenset({2}))
        binary_tree.add_vertex(frozenset({3}))
        binary_tree.add_vertex(frozenset({4}))
        binary_tree.add_vertex(frozenset({10}))
        binary_tree.add_vertex(frozenset({1, 2}))
        binary_tree.add_undirected(frozenset({2}), frozenset({1, 2}))
        binary_tree.add_undirected(frozenset({2}), frozenset({3}))
        binary_tree.add_undirected(frozenset({3}), frozenset({4}))
        binary_tree.add_undirected(frozenset({3}), frozenset({10}))
        decomposition = DecompositionBTB({})
        decomposition.tree = binary_tree
        decomposition.contract_tree_edge_from_lattice(6, {5}, self.lattice)
        self.assertIn(frozenset({1, 2}), decomposition.tree.undirected[frozenset({2, 3})])
        self.assertIn(frozenset({2, 3}), decomposition.tree.directed[frozenset({3})])
        self.assertIn(frozenset({3}), decomposition.tree.undirected[frozenset({10})])
        self.assertIn(frozenset({3}), decomposition.tree.undirected[frozenset({4})])
        self.assertNotIn(frozenset({2}), decomposition.tree.vertices)

    def test_contraction_trees(self):
        small_binary_lattice = Lattice((1, 2, 3, 4, 5, 'bottom', 'top'), (
            ('bottom', 1), ('bottom', 2), ('bottom', 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 'top'), (5, 'top')))
        tree = {1: [2],
                2: [1, 3],
                3: [2]}
        decomposition = DecompositionBTB(tree)
        decomposition.algo_from_lattice(small_binary_lattice)
        support = BinaryMixedTree(tree)
        self.assertEqual(decomposition.history[0], support)
        first_1 = BinaryMixedTree({})
        first_1.add_vertex(frozenset({1, 2}))
        first_1.add_vertex(frozenset({2}))
        first_1.add_vertex(frozenset({3}))
        first_1.add_directed(frozenset({2}), frozenset({1, 2}))
        first_1.add_undirected(frozenset({2}), frozenset({3}))
        first_2 = BinaryMixedTree({})
        first_2.add_vertex(frozenset({2, 3}))
        first_2.add_vertex(frozenset({2}))
        first_2.add_vertex(frozenset({1}))
        first_2.add_directed(frozenset({2}), frozenset({2, 3}))
        first_2.add_undirected(frozenset({1}), frozenset({2}))
        self.assertTrue(decomposition.history[1] == first_1 or decomposition.history[1] == first_2)
        second = BinaryMixedTree({})
        second.add_vertex(frozenset({1, 2}))
        second.add_vertex(frozenset({3, 2}))
        second.add_undirected(frozenset({1, 2}), frozenset({2, 3}))
        self.assertEqual(decomposition.history[2], second)
        last = BinaryMixedTree({})
        last.add_vertex(frozenset({1, 2, 3}))
        self.assertEqual(decomposition.history[3], last)
        self.assertTrue(decomposition.order == [frozenset({1, 2}), frozenset({2, 3}), frozenset({1, 2, 3})]
                        or decomposition.order == [frozenset({3, 2}), frozenset({2, 1}), frozenset({1, 2, 3})])

    def test_contraction_trees_more_specific_order(self):
        binary_atomistic_lattice = Lattice(
            vertices=['BOTTOM', 16, 17, 18, 3, 4, 1, 14, 19, 15, 0, 5, 11, 12, 2, 6, 9, 8, 13, 7],
            edges=[('BOTTOM', 16), ('BOTTOM', 17), ('BOTTOM', 18), ('BOTTOM', 3), ('BOTTOM', 4), ('BOTTOM', 1),
                   ('BOTTOM', 14), ('BOTTOM', 19), ('BOTTOM', 15), (4, 0), (1, 0), (1, 5), (14, 5), (5, 11), (11, 6),
                   (19, 11), (15, 6), (0, 12), (11, 12), (12, 2), (3, 2), (2, 9), (18, 9), (9, 8), (17, 8), (8, 13),
                   (6, 13), (13, 'TOP'), (7, 'TOP'), (5, 7), (16, 7)])
        support_tree = binary_atomistic_lattice.support_tree()
        decomposition = DecompositionBTB.init_from_graph_object(support_tree)
        decomposition.algo_from_lattice(binary_atomistic_lattice)
        self.assertEqual(len(decomposition.history[-1]), 1)

    def test_contraction_trees_move_edge(self):
        binary_atomistic_lattice = Lattice(
            vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18],
            edges=[('BOTTOM', 3), ('BOTTOM', 12), ('BOTTOM', 13), ('BOTTOM', 14),
                   ('BOTTOM', 15), ('BOTTOM', 16), ('BOTTOM', 17), ('BOTTOM', 18), (0, 6),
                   (6, 8), (1, 4), (1, 5), (2, 11), (3, 1), (3, 9), (4, 2),
                   (4, 7), (5, 0), (6, 2), (7, 'TOP'), (8, 11), (9, 8),
                   (11, 'TOP'), (12, 0), (13, 1), (14, 4), (15, 5), (16, 6),
                   (17, 7), (18, 9)])
        support_tree = binary_atomistic_lattice.support_tree()
        decomposition = DecompositionBTB.init_from_graph_object(support_tree)
        decomposition.algo_from_lattice(binary_atomistic_lattice)
        self.assertEqual(len(decomposition.history[-1]), 1)

    def test_order(self):
        tree = Graph(directed=False)
        tree.update(((1, 2), (2, 3)))
        decomposition = DecompositionBTB.init_from_graph_object(tree)
        decomposition.algo()
        self.assertSetEqual(decomposition.order[-1], frozenset({1, 2, 3}))
        self.assertTrue(decomposition.order[0] == frozenset({1, 2}) or decomposition.order[0] == frozenset({2, 3}))
