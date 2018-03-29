import unittest


from tbs.graph import Graph, random_tree, tree_from_prufer, prufer_from_tree, connected_parts


class TestCreation(unittest.TestCase):
    def test_empty_tree(self):
        self.assertEqual(Graph(), random_tree([]))


class TestPrufer(unittest.TestCase):
    def test_one_and_two_vertex_tree(self):
        self.assertEqual(Graph([1]), tree_from_prufer([], [1]))
        self.assertEqual(Graph([1, 2], [[1, 2]]), tree_from_prufer([], [1, 2]))

    def test_no_last_edge(self):
        self.assertEqual(Graph([1, 2, 3], [(1, 2), (2, 3)]), tree_from_prufer([1], [1, 2, 3]))

    def test_tree_from_prufer(self):
        prufer = [3, 3, 3, 4]
        vertices = list(range(1, len(prufer) + 3))

        tree = Graph.from_edges([(1, 4),
                                 (2, 4),
                                 (3, 4),
                                 (4, 5), (5, 6)])

        self.assertEqual(tree, tree_from_prufer(prufer, vertices))

    def test_prufer_from_tree_no_list(self):
        self.assertEqual([], prufer_from_tree(Graph([1]), [1]))
        self.assertEqual([], prufer_from_tree(Graph([1, 2], [[1, 2]]), [1, 2]))

    def test_prufer(self):
        self.assertEqual([3, 3, 3, 4], prufer_from_tree(Graph.from_edges([(1, 4),
                                                                          (2, 4),
                                                                          (3, 4),
                                                                          (4, 5), (5, 6)]),
                                                        [1, 2, 3, 4, 5, 6]))

    def test_random_tree_one_vertex(self):
        self.assertEqual(Graph([1]), random_tree([1]))

    def test_random_tree_two_vertex(self):
        self.assertEqual(Graph([1, 2], ([1, 2], )), random_tree([1, 2]))

    def test_random_tree(self):
        tree = random_tree([1, 2, 3, 4, 5, 6])
        self.assertEqual(frozenset([1, 2, 3, 4, 5, 6]), tree.vertices)
        self.assertEqual(5, len(tree.edges))
        self.assertTrue(1, len(connected_parts(tree)))
