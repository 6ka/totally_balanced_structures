import unittest
from TBS.graph import Graph
from TBS.binarize import max_intersection, is_binary, element_is_binary, bottom_up_element_binarization, \
    binarize_element, binarize, bottom_up_binarization, top_down_binarization, bfs_binarization, \
    move_sup_irreducibles_to_atoms, atoms, flat_contraction_order, is_flat, contraction_order, support_tree, \
    contract_edge, contraction_trees, dlo_support_tree_neighbour, dlo_support_tree
from tree import find_root
from TBS.lattice import dual_lattice, isa_lattice, sup_irreducible_clusters
from TBS.randomize import random_dismantable_lattice


class TestBinarize(unittest.TestCase):
    @staticmethod
    def new_lattice():
        lattice = Graph(directed=True)
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
        self.dual_lattice = dual_lattice(self.lattice)

    def test_atoms(self):
        self.assertSetEqual(atoms(self.lattice), {1, 2, 3, 4})
        self.assertSetEqual(atoms(self.lattice, "bottom"), {1, 2, 3, 4})

    def test_max_intersection(self):
        antichain = [{0, 1, 2, 3}, {6, 7}, {3, 4, 5, 6}, {2, 3, 4, 8, 9}, {9, 10}]
        for i in range(5):
            max_inter = max_intersection(antichain)
            self.assertIn(max_inter, {(0, 3), (3, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)})

    def test_max_intersection_with_equality(self):
        antichain = [{0, 1}, {0, 1}, {0, 2}]
        for i in range(5):
            max_inter = max_intersection(antichain)
            self.assertIn(max_inter, {(0, 1), (1, 0)})

    def test_is_binary(self):
        self.assertFalse(is_binary(self.lattice))
        self.assertTrue(is_binary(self.lattice.restriction(["bottom", 2, 3, 5, 6, 8])))

    def test_element_is_binary(self):
        self.assertTrue(element_is_binary(self.lattice, 5, self.dual_lattice))
        self.assertTrue(element_is_binary(self.lattice, 6, self.dual_lattice))
        self.assertTrue(element_is_binary(self.lattice, 4, self.dual_lattice))
        self.assertFalse(element_is_binary(self.lattice, 2, self.dual_lattice))
        self.assertFalse(element_is_binary(self.lattice, "bottom", self.dual_lattice))

    def test_element_is_binary_no_dual(self):
        self.assertTrue(element_is_binary(self.lattice, 5))
        self.assertTrue(element_is_binary(self.lattice, 6))
        self.assertTrue(element_is_binary(self.lattice, 4))
        self.assertFalse(element_is_binary(self.lattice, 2))
        self.assertFalse(element_is_binary(self.lattice, "bottom"))

    def test_bottom_up_element_binarization(self):
        binarized_2_lattice = bottom_up_element_binarization(self.lattice, 2)
        self.assertLessEqual(len(binarized_2_lattice[2]), 2)
        self.assertNotIn(7, binarized_2_lattice[10])
        self.assertTrue(isa_lattice(binarized_2_lattice))

    def test_bottom_up_binary_element_binarization(self):
        binarized_5_lattice = bottom_up_element_binarization(self.lattice, 5)
        self.assertLessEqual(len(binarized_5_lattice[2]), 5)
        self.assertTrue(isa_lattice(binarized_5_lattice))

    def test_top_down_element_binarization(self):
        self.lattice.update((('bottom', 10), (10, 7), (10, 11), (11, 'top')))
        binarized_7_lattice = binarize_element(self.lattice, 7)
        self.assertTrue(element_is_binary(binarized_7_lattice, 7, dual_lattice(binarized_7_lattice)))
        self.assertTrue(isa_lattice(binarized_7_lattice))

    def test_bfs_binarization(self):
        def element_binarization(lattice, vertex):
            lattice.remove(vertex)
            return lattice

        def condition(*unused):
            return True

        empty = bfs_binarization(self.lattice, condition, element_binarization, ignored_elements={})
        self.assertEqual(len(empty), 0)

    def test_bfs_binarization_with_ignored_elements(self):
        def element_binarization(lattice, vertex):
            lattice.remove(vertex)
            return lattice

        def condition(*unused):
            return True

        visited = bfs_binarization(self.lattice, condition, element_binarization, ignored_elements={1, 2})
        self.assertEqual(len(visited), 2)

    def test_binarize_element(self):
        self.lattice.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2), ('bottom', 2)))
        binarized_2_lattice = binarize_element(self.lattice, 2)
        self.assertTrue(element_is_binary(binarized_2_lattice, 2, dual_lattice(binarized_2_lattice)))
        self.assertTrue(isa_lattice(binarized_2_lattice))

    def test_binarize_binary_element(self):
        binarized_5_lattice = binarize_element(self.lattice, 5)
        self.assertTrue(element_is_binary(binarized_5_lattice, 5, dual_lattice(binarized_5_lattice)))
        self.assertTrue(isa_lattice(binarized_5_lattice))

    def test_binarize_with_one_element_bottom_up_not_binary(self):
        binarized_lattice = binarize(self.lattice)
        self.assertTrue(is_binary(binarized_lattice))
        self.assertTrue(isa_lattice(binarized_lattice))

    def test_binarize_with_one_element_not_binary(self):
        self.lattice.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2), ('bottom', 2)))
        binarized_lattice = binarize(self.lattice)
        self.assertTrue(is_binary(binarized_lattice))
        self.assertTrue(isa_lattice(binarized_lattice))

    def test_binarize(self):
        binarized_lattice = binarize(self.lattice)
        self.assertTrue(is_binary(binarized_lattice))
        self.assertTrue(isa_lattice(binarized_lattice))

    def test_random_binarize(self):
        for i in range(10):
            lattice = random_dismantable_lattice(20)
            binarized_lattice = binarize(lattice)
            self.assertTrue(is_binary(binarized_lattice))
            self.assertTrue(isa_lattice(binarized_lattice))

    def test_binarize_with_ignored_elements(self):
        binarized_ignore_2 = binarize(self.lattice, {2})
        self.assertTrue(isa_lattice(binarized_ignore_2))
        self.assertFalse(element_is_binary(binarized_ignore_2, 2))
        for element in binarized_ignore_2:
            if element != 2 and element != 'bottom':
                self.assertTrue(element_is_binary(binarized_ignore_2, element))
        binarized_ignore_78 = binarize(self.lattice, {7, 8})
        self.assertTrue(isa_lattice(binarized_ignore_78))
        self.assertTrue(is_binary(binarized_ignore_78))

    def test_bottom_up_binarization_with_ignored_elements(self):
        binarized_ignore_2 = bottom_up_binarization(self.lattice, {2})
        self.assertTrue(isa_lattice(binarized_ignore_2))
        self.assertFalse(len(binarized_ignore_2[2]) <= 2)
        for element in binarized_ignore_2:
            if element != 2 and element != 'bottom':
                self.assertTrue(len(binarized_ignore_2[element]) <= 2)
        binarized_ignore_78 = bottom_up_binarization(self.lattice, {7, 8})
        self.assertTrue(isa_lattice(binarized_ignore_78))
        self.assertTrue(is_binary(binarized_ignore_78))

    def test_random_bottom_up_binarization(self):
        for i in range(10):
            lattice = random_dismantable_lattice(20)
            binarized_lattice = bottom_up_binarization(lattice)
            for element in binarized_lattice:
                if element != 'BOTTOM':
                    self.assertLessEqual(len(binarized_lattice[element]), 2)
            self.assertTrue(isa_lattice(binarized_lattice))

    def test_random_top_down_binarization(self):
        for i in range(10):
            lattice = random_dismantable_lattice(20)
            binarized_lattice = top_down_binarization(lattice)
            for element in binarized_lattice:
                if element != 'BOTTOM':
                    self.assertLessEqual(len(dual_lattice(binarized_lattice)[element]), 2)
            self.assertTrue(isa_lattice(binarized_lattice))

    def test_move_sup_irreducibles_to_atoms(self):
        flat_lattice = move_sup_irreducibles_to_atoms(self.lattice)
        self.assertSetEqual(atoms(flat_lattice), {1, 2, 3, 4, 10})
        self.assertListEqual(flat_lattice[10], [9])

    def test_flat_contraction_order(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        order = flat_contraction_order(self.lattice)
        self.assertTrue(order.index(8) > order.index(5))
        self.assertTrue(order.index(8) > order.index(6))
        self.assertTrue(order.index(5) > order.index(11))
        self.assertTrue(order.index(6) > order.index(11))
        self.assertTrue(order.index(9) > order.index(7))
        self.assertNotIn(1, order)
        self.assertNotIn(2, order)
        self.assertNotIn(3, order)
        self.assertNotIn(4, order)
        self.assertNotIn(10, order)

    def test_is_flat(self):
        self.assertFalse(is_flat(self.lattice))
        self.lattice.update((('bottom', 10), (10, 9)))
        self.assertTrue(is_flat(self.lattice))
        self.assertTrue(is_flat(self.lattice, "bottom"))

    def test_contraction_order(self):
        order = contraction_order(self.lattice)
        self.assertTrue(order.index(8) > order.index(5))
        self.assertTrue(order.index(8) > order.index(6))
        self.assertTrue(order.index(9) > order.index(7))

    def test_contraction_order_with_red_path(self):
        flat_binarized_lattice = Graph(vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15],
                                       edges=[('BOTTOM', 3, None), ('BOTTOM', 10, None), ('BOTTOM', 11, None),
                                              ('BOTTOM', 12, None),
                                              ('BOTTOM', 13, None), ('BOTTOM', 14, None), ('BOTTOM', 15, None),
                                              (0, 9, None), (1, 5, None),
                                              (1, 8, None), (2, 'TOP', None), (3, 1, None), (3, 4, None), (4, 2, None),
                                              (5, 'TOP', None),
                                              (6, 9, None), (8, 0, None), (8, 6, None), (9, 2, None), (10, 0, None),
                                              (11, 1, None),
                                              (12, 4, None), (13, 5, None), (14, 6, None), (15, 8, None)],
                                       directed=True)
        order = contraction_order(flat_binarized_lattice)
        for i in [0, 2, 5, 6, 8, 9]:
            self.assertTrue(order.index(1) < order.index(i))
            self.assertTrue(order.index(4) < order.index(i))
        self.assertTrue(order.index(6) > order.index(5))
        self.assertTrue(order.index(0) > order.index(5))

    def test_support_tree(self):
        tree = support_tree(move_sup_irreducibles_to_atoms(self.lattice))
        self.assertTrue(tree.isa_edge(1, 2))
        self.assertTrue(tree.isa_edge(3, 2))
        self.assertTrue(tree.isa_edge(4, 2))
        self.assertTrue(tree.isa_edge(10, 2) or tree.isa_edge(10, 4))
        self.assertFalse(tree.isa_edge(1, 3))
        self.assertFalse(tree.isa_edge(1, 4))
        self.assertFalse(tree.isa_edge(3, 4))
        self.assertFalse(tree.isa_edge(10, 1))
        self.assertFalse(tree.isa_edge(10, 3))
        self.assertFalse(tree.isa_edge(10, 2) and tree.isa_edge(10, 4))
        tree = support_tree(move_sup_irreducibles_to_atoms(self.lattice), 'bottom')
        self.assertTrue(tree.isa_edge(1, 2))
        self.assertTrue(tree.isa_edge(3, 2))
        self.assertTrue(tree.isa_edge(4, 2))
        self.assertTrue(tree.isa_edge(10, 2) or tree.isa_edge(10, 4))
        self.assertFalse(tree.isa_edge(1, 3))
        self.assertFalse(tree.isa_edge(1, 4))
        self.assertFalse(tree.isa_edge(3, 4))
        self.assertFalse(tree.isa_edge(10, 1))
        self.assertFalse(tree.isa_edge(10, 3))
        self.assertFalse(tree.isa_edge(10, 2) and tree.isa_edge(10, 4))

    def test_find_root(self):
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5, 6], edges=((0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)))
        root = find_root(tree)
        self.assertEqual(root, 0)
        tree = Graph(vertices=[0, 1, 2, 3, 4, 5], edges=((0, 1), (0, 2), (0, 3), (1, 4), (1, 5)))
        root = find_root(tree)
        self.assertTrue(root == 0 or root == 1)

    def test_contract_edge_one_disappears(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        self.dual_lattice = dual_lattice(self.lattice)
        tree = Graph((1, 2, 3, 4, 10, 12), ((2, 12), (1, 2), (2, 3), (2, 4), (4, 10)), False)
        contract_24_tree = contract_edge(tree, 7, self.lattice, self.dual_lattice, set())
        self.assertTrue(contract_24_tree.isa_edge(7, 2))
        self.assertTrue(contract_24_tree.isa_edge(2, 1))
        self.assertTrue(contract_24_tree.isa_edge(2, 3))
        self.assertTrue(contract_24_tree.isa_edge(2, 12))
        self.assertTrue(contract_24_tree.isa_edge(7, 10))
        self.assertFalse(contract_24_tree.isa_vertex(4))
        self.assertTrue(len(tree.edges()) == 5)

    def test_contract_edge_both_disappear(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        self.dual_lattice = dual_lattice(self.lattice)
        tree = Graph((5, 6, 7, 10), ((5, 6), (6, 7), (7, 10)), False)
        contract_56_tree = contract_edge(tree, 8, self.lattice, self.dual_lattice, {5, 6, 7, 11})
        self.assertTrue(contract_56_tree.isa_edge(8, 7))
        self.assertTrue(contract_56_tree.isa_edge(10, 7))
        self.assertFalse(contract_56_tree.isa_vertex(5))
        self.assertFalse(contract_56_tree.isa_vertex(6))
        self.assertTrue(len(tree.edges()) == 2)

    def test_contract_edge_both_stay(self):
        self.lattice.update(((2, 7), ('bottom', 10), (10, 9), (3, 7)))
        self.dual_lattice = dual_lattice(self.lattice)
        tree = Graph((1, 2, 3, 4, 10), ((1, 2), (2, 3), (3, 4), (3, 10)), False)
        contract_23_tree = contract_edge(tree, 6, self.lattice, self.dual_lattice, set())
        self.assertTrue(contract_23_tree.isa_edge(1, 2))
        self.assertTrue(contract_23_tree.isa_edge(2, 6))
        self.assertTrue(contract_23_tree.isa_edge(6, 3))
        self.assertTrue(contract_23_tree.isa_edge(3, 10))
        self.assertTrue(contract_23_tree.isa_edge(3, 4))
        self.assertFalse(contract_23_tree.isa_edge(2, 3))
        self.assertTrue(len(tree.edges()) == 5)

    def test_contract_edge_one_already_used(self):
        self.lattice.update(((2, 7), ('bottom', 10), (10, 9), (3, 7)))
        self.dual_lattice = dual_lattice(self.lattice)
        tree = Graph((2, 3, 4, 5, 10), ((5, 2), (2, 3), (3, 4), (3, 10)), False)
        contract_23_tree = contract_edge(tree, 6, self.lattice, self.dual_lattice, {5})
        self.assertTrue(contract_23_tree.isa_edge(5, 6))
        self.assertTrue(contract_23_tree.isa_edge(6, 3))
        self.assertTrue(contract_23_tree.isa_edge(3, 10))
        self.assertTrue(contract_23_tree.isa_edge(3, 4))
        self.assertFalse(contract_23_tree.isa_vertex(2))
        self.assertTrue(len(tree.edges()) == 4)

    def test_contraction_trees(self):
        small_binary_lattice = Graph((1, 2, 3, 4, 5, 'bottom', 'top'), (
            ('bottom', 1), ('bottom', 2), ('bottom', 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 'top'), (5, 'top')),
                                     directed=True)
        trees = contraction_trees(small_binary_lattice, bottom='bottom')
        support = Graph((1, 2, 3), ((1, 2), (2, 3)))
        self.assertEqual(trees[0], support)
        first_1 = Graph((4, 2, 3), ((4, 2), (2, 3)))
        first_2 = Graph((1, 2, 5), ((1, 2), (2, 5)))
        self.assertTrue(trees[1] == first_1 or trees[1] == first_2)
        second = Graph((4, 5), ((4, 5),))
        self.assertEqual(trees[2], second)
        last = Graph(('top',), ())
        self.assertEqual(trees[3], last)

    def test_contraction_trees_more_specific_order(self):
        # lattice = Graph(vertices=['BOTTOM', 1, 3, 4, 0, 2, 5, 9, 6, 7, 'TOP', 8],
        #                 edges=[('BOTTOM', 1, None), ('BOTTOM', 3, None), ('BOTTOM', 4, None), (1, 0, None),
        #                        (1, 5, None), (3, 2, None), (4, 0, None), (0, 2, None), (2, 9, None), (5, 2, None),
        #                        (5, 6, None), (5, 7, None), (9, 8, None), (6, 'TOP', None), (7, 'TOP', None),
        #                        (8, 'TOP', None)], directed=True)
        flat_binarized_lattice = Graph(
            vertices=['BOTTOM', 16, 17, 18, 3, 4, 1, 14, 19, 15, 0, 5, 11, 12, 2, 6, 9, 8, 13, 7],
            edges=[('BOTTOM', 16), ('BOTTOM', 17), ('BOTTOM', 18), ('BOTTOM', 3), ('BOTTOM', 4), ('BOTTOM', 1),
                   ('BOTTOM', 14), ('BOTTOM', 19), ('BOTTOM', 15), (4, 0), (1, 0), (1, 5), (14, 5), (5, 11), (11, 6),
                   (19, 11), (15, 6), (0, 12), (11, 12), (12, 2), (3, 2), (2, 9), (18, 9), (9, 8), (17, 8), (8, 13),
                   (6, 13), (13, 'TOP'), (7, 'TOP'), (5, 7), (16, 7)], directed=True)
        trees = contraction_trees(flat_binarized_lattice)
        self.assertEqual(len(trees[-1]), 1)

    def test_contraction_trees_move_edge(self):
        # lattice = Graph(vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        #                 edges=[('BOTTOM', 3, None), (0, 6, None), (6, 8, None), (1, 4, None), (1, 5, None),
        #                        (2, 'TOP', None), (3, 1, None), (3, 9, None), (4, 2, None), (4, 7, None), (5, 0, None),
        #                        (6, 2, None), (7, 'TOP', None), (8, 'TOP', None), (9, 8, None)], directed=True)
        flat_binarized_lattice = Graph(
            vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18],
            edges=[('BOTTOM', 3, None), ('BOTTOM', 12, None), ('BOTTOM', 13, None), ('BOTTOM', 14, None),
                   ('BOTTOM', 15, None), ('BOTTOM', 16, None), ('BOTTOM', 17, None), ('BOTTOM', 18, None), (0, 6, None),
                   (6, 8, None), (1, 4, None), (1, 5, None), (2, 11, None), (3, 1, None), (3, 9, None), (4, 2, None),
                   (4, 7, None), (5, 0, None), (6, 2, None), (7, 'TOP', None), (8, 11, None), (9, 8, None),
                   (11, 'TOP', None), (12, 0, None), (13, 1, None), (14, 4, None), (15, 5, None), (16, 6, None),
                   (17, 7, None), (18, 9, None)], directed=True)
        trees = contraction_trees(flat_binarized_lattice, order=[9, 1, 5, 0, 6, 8, 4, 2, 7, 11, 'TOP'])
        print(trees[-1], [vertex for vertex in trees[-1]])
        self.assertEqual(len(trees[-1]), 1)

    def test_dlo_support_tree_neighbour_direct(self):
        flat_binarized_lattice = Graph(
            vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18],
            edges=[('BOTTOM', 3, None), ('BOTTOM', 12, None), ('BOTTOM', 13, None), ('BOTTOM', 14, None),
                   ('BOTTOM', 15, None), ('BOTTOM', 16, None), ('BOTTOM', 17, None), ('BOTTOM', 18, None), (0, 6, None),
                   (6, 8, None), (1, 4, None), (1, 5, None), (2, 11, None), (3, 1, None), (3, 9, None), (4, 2, None),
                   (4, 7, None), (5, 0, None), (6, 2, None), (7, 'TOP', None), (8, 11, None), (9, 8, None),
                   (11, 'TOP', None), (12, 0, None), (13, 1, None), (14, 4, None), (15, 5, None), (16, 6, None),
                   (17, 7, None), (18, 9, None)], directed=True)
        classes = sup_irreducible_clusters(flat_binarized_lattice)
        row_order = [17, 18, 14, 16, 12, 15, 13, 3]
        assert dlo_support_tree_neighbour(flat_binarized_lattice, row_order, 17, classes) == 14
        assert dlo_support_tree_neighbour(flat_binarized_lattice, row_order, 18, classes) == 3

    def test_dlo_support_tree_neighbour_two_distinct_clusters(self):
        flat_binarized_lattice = Graph(vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], edges=[('BOTTOM', 0, None), ('BOTTOM', 3, None), ('BOTTOM', 5, None), ('BOTTOM', 17, None), ('BOTTOM', 18, None), ('BOTTOM', 19, None), ('BOTTOM', 20, None), ('BOTTOM', 21, None), ('BOTTOM', 22, None), ('BOTTOM', 23, None), ('BOTTOM', 24, None), ('BOTTOM', 25, None), (0, 2, None), (1, 9, None), (1, 14, None), (2, 8, None), (3, 7, None), (3, 10, None), (4, 11, None), (4, 13, None), (5, 1, None), (6, 16, None), (7, 4, None), (8, 'TOP', None), (9, 12, None), (10, 16, None), (11, 6, None), (12, 'TOP', None), (13, 9, None), (14, 12, None), (16, 1, None), (17, 2, None), (18, 4, None), (19, 6, None), (20, 7, None), (21, 8, None), (22, 10, None), (23, 11, None), (24, 13, None), (25, 14, None)], directed=True)
        classes = sup_irreducible_clusters(flat_binarized_lattice)
        row_order = [25,24,5,22,19,23,18,20,3,21,17,0]
        assert dlo_support_tree_neighbour(flat_binarized_lattice, row_order, 3, classes) == 21

    def test_dlo_support_tree(self):
        flat_binarized_lattice = Graph(
            vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18],
            edges=[('BOTTOM', 3, None), ('BOTTOM', 12, None), ('BOTTOM', 13, None), ('BOTTOM', 14, None),
                   ('BOTTOM', 15, None), ('BOTTOM', 16, None), ('BOTTOM', 17, None), ('BOTTOM', 18, None), (0, 6, None),
                   (6, 8, None), (1, 4, None), (1, 5, None), (2, 11, None), (3, 1, None), (3, 9, None), (4, 2, None),
                   (4, 7, None), (5, 0, None), (6, 2, None), (7, 'TOP', None), (8, 11, None), (9, 8, None),
                   (11, 'TOP', None), (12, 0, None), (13, 1, None), (14, 4, None), (15, 5, None), (16, 6, None),
                   (17, 7, None), (18, 9, None)], directed=True)
        classes = sup_irreducible_clusters(flat_binarized_lattice)
        support_tree = dlo_support_tree(flat_binarized_lattice)
        for cls in classes:
            if cls != 'BOTTOM':
                assert len(support_tree.connected_parts(list(classes[cls]))) == 1
