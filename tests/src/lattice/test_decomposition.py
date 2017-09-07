import unittest
from TBS.tree_decomposition import DecompositionBTB


class TestDecomposition(unittest.TestCase):
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