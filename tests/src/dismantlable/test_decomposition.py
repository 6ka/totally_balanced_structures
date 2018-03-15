import unittest

from tbs.dismantlable import DismantlableLattice, DecompositionBTB, BinaryMixedTree
from tbs.lattice import isa_lattice_directed_comparability_graph
from tbs.graph import Graph, DirectedGraph


class TestDecomposition(unittest.TestCase):
    def test_init_from_graph(self):
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5, 6], edges=((0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)))
        decomposition = DecompositionBTB.build_from_tree(tree)
        self.assertEqual(BinaryMixedTree(tree), decomposition.history[0])
        self.assertEqual({frozenset([0, 1, 2, 3, 4, 5, 6])}, decomposition.history[-1].vertices)

    def test_final_lattice(self):
        decomposition = DecompositionBTB.build_from_tree(
            Graph(vertices=[0, 1, 2, 3, 4], edges=((0, 1), (0, 2), (0, 3), (1, 4))))

        self.assertTrue(isa_lattice_directed_comparability_graph(decomposition.hase_diagram))

    def test_remove_directed(self):
        tree = Graph()
        tree.update(((5, 7), (5, 2), (5, 3), (3, 6), (3, 8), (3, 4), (3, 1), (3, 9), (9, 0)))
        decomposition = DecompositionBTB(tree)
        decomposition.tree.remove_undirected(frozenset([3]), frozenset([9]))
        decomposition.tree.add_directed(frozenset([3]), frozenset([9]))

        decomposition.step(frozenset([3]), frozenset([5]), lambda u: frozenset())

        self.assertNotIn(frozenset([3]), decomposition.tree.vertices)
        self.assertIn(frozenset([3, 5]), decomposition.tree.vertices)

        self.assertEqual(0, len(decomposition.tree(frozenset([9]), undirected=False, begin=False, end=True)))

        self.assertEqual(set(frozenset([x]) for x in [1, 4, 6, 8, 9]),
                         decomposition.tree(frozenset([3, 5]), undirected=True, begin=False, end=False))

    def test_contract_edge_one_disappears(self):
        tree = Graph().update(((1, 2), (2, 12), (2, 3), (2, 4), (4, 10)))
        decomposition = DecompositionBTB(tree)

        decomposition.step(frozenset([2]), frozenset([4]),
                           lambda x: x == frozenset([4]) and [frozenset([10])] or [])

        self.assertIn(frozenset({1}), decomposition.tree(frozenset({2}), undirected=True, begin=False, end=False))
        self.assertIn(frozenset({12}), decomposition.tree(frozenset({2}), undirected=True, begin=False, end=False))
        self.assertIn(frozenset({3}), decomposition.tree(frozenset({2}), undirected=True, begin=False, end=False))
        self.assertIn(frozenset({2, 4}), decomposition.tree(frozenset({10}), undirected=True, begin=False, end=False))
        self.assertNotIn(frozenset({4}), decomposition.tree.vertices)
        self.assertEqual(len(decomposition.tree.vertices), 6)

    def test_contract_edge_both_disappear(self):
        binary_tree = BinaryMixedTree({})
        binary_tree.add(frozenset({1, 2, 12}))
        binary_tree.add(frozenset({3, 2, 12}))
        binary_tree.add(frozenset({2, 4}))
        binary_tree.add(frozenset({10}))
        binary_tree.add_undirected(frozenset({1, 2, 12}), frozenset({2, 3, 12}))
        binary_tree.add_undirected(frozenset({3, 2, 12}), frozenset({2, 4}))
        binary_tree.add_undirected(frozenset({2, 4}), frozenset({10}))
        decomposition = DecompositionBTB(Graph())
        decomposition.tree = binary_tree
        decomposition.step(frozenset([1, 2, 12]), frozenset([2, 3, 12]),
                           lambda x: x == frozenset([2, 3, 12]) and [frozenset([2, 4])] or [])

        self.assertIn(frozenset({1, 2, 3, 12}),
                      decomposition.tree(frozenset({2, 4}), undirected=True, begin=False, end=False))
        self.assertIn(frozenset({10}), decomposition.tree(frozenset({2, 4}), undirected=True, begin=False, end=False))
        self.assertNotIn(frozenset({1, 2, 12}), decomposition.tree.vertices)
        self.assertNotIn(frozenset({2, 3, 12}), decomposition.tree.vertices)
        self.assertTrue(len(decomposition.tree.vertices) == 3)

    def test_contract_edge_both_stay(self):
        tree = Graph()
        tree.update(((1, 2), (2, 3), (3, 4), (3, 10)))
        decomposition = DecompositionBTB(tree)
        decomposition.step(frozenset([2]), frozenset([3]), lambda x: [])

        self.assertIn(frozenset({1}), decomposition.tree(frozenset({2}), undirected=True, begin=False, end=False))
        self.assertIn(frozenset({2, 3}), decomposition.tree(frozenset({2}), undirected=False, begin=True, end=False))
        self.assertIn(frozenset({2, 3}), decomposition.tree(frozenset({3}), undirected=False, begin=True, end=False))
        self.assertIn(frozenset({3}), decomposition.tree(frozenset({10}), undirected=True, begin=False, end=False))
        self.assertIn(frozenset({3}), decomposition.tree(frozenset({4}), undirected=True, begin=False, end=False))
        self.assertNotIn(frozenset({2}), decomposition.tree(frozenset({3}), undirected=True, begin=False, end=False))

    def test_reconstruct_lattice(self):
        lattice = DismantlableLattice(DirectedGraph.from_edges([("bottom", 1),
                                                                ("bottom", 2),
                                                                ("bottom", 3),
                                                                ("bottom", 4),
                                                                ('bottom', 10),
                                                                ('bottom', 12),
                                                                (1, 5),
                                                                (2, 7),
                                                                (3, 6),
                                                                (4, 7),
                                                                (10, 9),
                                                                (12, 11),
                                                                (5, 8),
                                                                (6, 8),
                                                                (7, 9),
                                                                (8, "top"),
                                                                (9, "top"),
                                                                (2, 11), (11, 5), (11, 6)]))

        hase_diagram = DirectedGraph.from_edges([(frozenset(), frozenset([1])),
                                                 (frozenset(), frozenset([2])),
                                                 (frozenset(), frozenset([3])),
                                                 (frozenset(), frozenset([4])),
                                                 (frozenset(), frozenset([10])),
                                                 (frozenset(), frozenset([12])),
                                                 (frozenset([1]), frozenset([1, 2, 12])),
                                                 (frozenset([2]), frozenset([2, 4])),
                                                 (frozenset([2]), frozenset([2, 12])),
                                                 (frozenset([3]), frozenset([2, 3, 12])),
                                                 (frozenset([4]), frozenset([2, 4])),
                                                 (frozenset([10]), frozenset([2, 4, 10])),
                                                 (frozenset([12]), frozenset([2, 12])),
                                                 (frozenset([1, 2, 12]), frozenset([1, 2, 3, 12])),
                                                 (frozenset([2, 3, 12]), frozenset([1, 2, 3, 12])),
                                                 (frozenset([2, 4]), frozenset([2, 4, 10])),
                                                 (frozenset([1, 2, 3, 12]), frozenset([1, 2, 3, 4, 10, 12])),
                                                 (frozenset([2, 4, 10]), frozenset([1, 2, 3, 4, 10, 12])),
                                                 (frozenset([2, 12]), frozenset([1, 2, 12])),
                                                 (frozenset([2, 12]), frozenset([2, 3, 12])),
                                                 ])

        decomposition = DecompositionBTB.build_from_binary_lattice(lattice)

        self.assertTrue(isa_lattice_directed_comparability_graph(hase_diagram))
        self.assertEqual(hase_diagram, decomposition.hase_diagram)
        self.assertTrue(isa_lattice_directed_comparability_graph(decomposition.hase_diagram))
