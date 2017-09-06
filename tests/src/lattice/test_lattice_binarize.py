from TBS.lattice import Lattice, max_intersection
from TBS.graph import Graph
import unittest


class TestLatticeBinarize(unittest.TestCase):
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
        self.assertFalse(self.lattice.is_binary())
        self.lattice.remove(2)
        self.assertTrue(self.lattice.is_binary())

    def test_element_is_binary(self):
        self.assertTrue(self.lattice.element_is_binary(5))
        self.assertTrue(self.lattice.element_is_binary(6))
        self.assertTrue(self.lattice.element_is_binary(4))
        self.assertFalse(self.lattice.element_is_binary(2))
        self.assertFalse(self.lattice.element_is_binary("bottom"))

    def test_bottom_up_element_binarization(self):
        self.lattice.bottom_up_element_binarization(2)
        self.assertLessEqual(len(self.lattice[2]), 2)
        self.assertNotIn(7, self.lattice[10])
        self.assertTrue(self.lattice.is_a_lattice())

    def test_bottom_up_binary_element_binarization(self):
        self.lattice.bottom_up_element_binarization(5)
        self.assertLessEqual(len(self.lattice[2]), 5)
        self.assertTrue(self.lattice.is_a_lattice())

    def test_top_down_element_binarization(self):
        self.lattice.update((('bottom', 10), (10, 7), (10, 11), (11, 'top')))
        self.lattice.binarize_element(7)
        self.assertTrue(self.lattice.element_is_binary(7))
        self.assertTrue(self.lattice.is_a_lattice())

    def test_binarize_element(self):
        self.lattice.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2), ('bottom', 2)))
        self.lattice.binarize_element(2)
        self.assertTrue(self.lattice.element_is_binary(2))
        self.assertTrue(self.lattice.is_a_lattice())

    def test_binarize_binary_element(self):
        self.lattice.binarize_element(5)
        self.assertTrue(self.lattice.element_is_binary(5))
        self.assertTrue(self.lattice.is_a_lattice())

    def test_binarize_with_one_element_bottom_up_not_binary(self):
        self.lattice.binarize()
        self.assertTrue(self.lattice.is_binary())
        self.assertTrue(self.lattice.is_a_lattice())

    def test_binarize_with_one_element_not_binary(self):
        self.lattice.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2), ('bottom', 2)))
        self.lattice.binarize()
        self.assertTrue(self.lattice.is_binary())
        self.assertTrue(self.lattice.is_a_lattice())

    def test_binarize(self):
        self.lattice.binarize()
        self.assertTrue(self.lattice.is_binary())
        self.assertTrue(self.lattice.is_a_lattice())

    def test_binarize_with_ignored_elements(self):
        self.lattice.binarize({2})
        self.assertTrue(self.lattice.is_a_lattice())
        self.assertFalse(self.lattice.element_is_binary(2))
        for element in self.lattice:
            if element != 2 and element != 'bottom':
                self.assertTrue(self.lattice.element_is_binary(element))

    def test_bottom_up_binarization(self):
        self.lattice.binarize_bottom_up()
        self.assertTrue(self.lattice.is_a_lattice())
        for element in self.lattice:
            if element != 'bottom':
                self.assertTrue(len(self.lattice[element]) <= 2)

    def test_bottom_up_binarization_with_ignored_elements(self):
        self.lattice.binarize_bottom_up({2})
        self.assertTrue(self.lattice.is_a_lattice())
        self.assertFalse(len(self.lattice[2]) <= 2)
        for element in self.lattice:
            if element != 2 and element != 'bottom':
                self.assertTrue(len(self.lattice[element]) <= 2)

    def test_top_down_binarization(self):
        self.lattice.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 4), (11, 4), (12, 4), ('bottom', 4)))
        self.lattice.binarize_top_down()
        self.assertTrue(self.lattice.is_a_lattice())
        for element in self.lattice:
            self.assertTrue(len(self.lattice.dual_lattice[element]) <= 2)
        self.assertTrue(len(self.lattice[2]) > 2)

    def test_other_successor(self):
        self.lattice.update(((2, 7),))
        self.assertEqual(self.lattice.other_successor(2, 5), 6)

    def test_atomistic_contraction_order(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        order = self.lattice.contraction_order()
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

    def test_contraction_order(self):
        order = self.lattice.contraction_order()
        self.assertTrue(order.index(8) > order.index(5))
        self.assertTrue(order.index(8) > order.index(6))
        self.assertTrue(order.index(9) > order.index(7))

    def test_contraction_order_with_red_path(self):
        binary_atomistic_lattice = Lattice()
        binary_atomistic_lattice.update((('BOTTOM', 3), ('BOTTOM', 10), ('BOTTOM', 11), ('BOTTOM', 12), ('BOTTOM', 13),
                                         ('BOTTOM', 14), ('BOTTOM', 15), (0, 9), (1, 5), (1, 8), (2, 'TOP'), (3, 1),
                                         (3, 4), (4, 2), (5, 'TOP'), (6, 9), (8, 0), (8, 6), (9, 2), (10, 0), (11, 1),
                                         (12, 4), (13, 5), (14, 6), (15, 8)))
        order = binary_atomistic_lattice.contraction_order()
        for i in [0, 2, 5, 6, 8, 9]:
            self.assertTrue(order.index(1) < order.index(i))
            self.assertTrue(order.index(4) < order.index(i))
        self.assertTrue(order.index(6) > order.index(5))
        self.assertTrue(order.index(0) > order.index(5))

    def test_contract_edge_one_disappears(self):
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        self.lattice.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        self.dual_lattice = self.lattice.dual_lattice
        tree = Graph((1, 2, 3, 4, 10, 12), ((2, 12), (1, 2), (2, 3), (2, 4), (4, 10)), False)
        contract_24_tree = self.lattice.contract_tree_edge(tree, 7, set())
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
        self.dual_lattice = self.lattice.dual_lattice
        tree = Graph((5, 6, 7, 10), ((5, 6), (6, 7), (7, 10)), False)
        contract_56_tree = self.lattice.contract_tree_edge(tree, 8, {5, 6, 7, 11})
        self.assertTrue(contract_56_tree.isa_edge(8, 7))
        self.assertTrue(contract_56_tree.isa_edge(10, 7))
        self.assertFalse(contract_56_tree.isa_vertex(5))
        self.assertFalse(contract_56_tree.isa_vertex(6))
        self.assertTrue(len(tree.edges()) == 2)

    def test_contract_edge_both_stay(self):
        self.lattice.update(((2, 7), ('bottom', 10), (10, 9), (3, 7)))
        tree = Graph((1, 2, 3, 4, 10), ((1, 2), (2, 3), (3, 4), (3, 10)), False)
        contract_23_tree = self.lattice.contract_tree_edge(tree, 6, set())
        self.assertTrue(contract_23_tree.isa_edge(1, 2))
        self.assertTrue(contract_23_tree.isa_edge(2, 6))
        self.assertTrue(contract_23_tree.isa_edge(6, 3))
        self.assertTrue(contract_23_tree.isa_edge(3, 10))
        self.assertTrue(contract_23_tree.isa_edge(3, 4))
        self.assertFalse(contract_23_tree.isa_edge(2, 3))
        self.assertTrue(len(tree.edges()) == 5)

    def test_contract_edge_one_already_used(self):
        self.lattice.update(((2, 7), ('bottom', 10), (10, 9), (3, 7)))
        tree = Graph((2, 3, 4, 5, 10), ((5, 2), (2, 3), (3, 4), (3, 10)), False)
        contract_23_tree = self.lattice.contract_tree_edge(tree, 6, {5})
        self.assertTrue(contract_23_tree.isa_edge(5, 6))
        self.assertTrue(contract_23_tree.isa_edge(6, 3))
        self.assertTrue(contract_23_tree.isa_edge(3, 10))
        self.assertTrue(contract_23_tree.isa_edge(3, 4))
        self.assertFalse(contract_23_tree.isa_vertex(2))
        self.assertTrue(len(tree.edges()) == 4)

    def test_contraction_trees(self):
        small_binary_lattice = Lattice((1, 2, 3, 4, 5, 'bottom', 'top'), (
            ('bottom', 1), ('bottom', 2), ('bottom', 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 'top'), (5, 'top')))
        trees = small_binary_lattice.contraction_trees()
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
        binary_atomistic_lattice = Lattice(
            vertices=['BOTTOM', 16, 17, 18, 3, 4, 1, 14, 19, 15, 0, 5, 11, 12, 2, 6, 9, 8, 13, 7],
            edges=[('BOTTOM', 16), ('BOTTOM', 17), ('BOTTOM', 18), ('BOTTOM', 3), ('BOTTOM', 4), ('BOTTOM', 1),
                   ('BOTTOM', 14), ('BOTTOM', 19), ('BOTTOM', 15), (4, 0), (1, 0), (1, 5), (14, 5), (5, 11), (11, 6),
                   (19, 11), (15, 6), (0, 12), (11, 12), (12, 2), (3, 2), (2, 9), (18, 9), (9, 8), (17, 8), (8, 13),
                   (6, 13), (13, 'TOP'), (7, 'TOP'), (5, 7), (16, 7)])
        trees = binary_atomistic_lattice.contraction_trees()
        self.assertEqual(len(trees[-1]), 1)

    def test_contraction_trees_move_edge(self):
        binary_atomistic_lattice = Lattice(
            vertices=['BOTTOM', 'TOP', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18],
            edges=[('BOTTOM', 3), ('BOTTOM', 12), ('BOTTOM', 13), ('BOTTOM', 14),
                   ('BOTTOM', 15), ('BOTTOM', 16), ('BOTTOM', 17), ('BOTTOM', 18), (0, 6),
                   (6, 8), (1, 4), (1, 5), (2, 11), (3, 1), (3, 9), (4, 2),
                   (4, 7), (5, 0), (6, 2), (7, 'TOP'), (8, 11), (9, 8),
                   (11, 'TOP'), (12, 0), (13, 1), (14, 4), (15, 5), (16, 6),
                   (17, 7), (18, 9)])
        trees = binary_atomistic_lattice.contraction_trees(order=[9, 1, 5, 0, 6, 8, 4, 2, 7, 11, 'TOP'])
        print(trees[-1], [vertex for vertex in trees[-1]])
        self.assertEqual(len(trees[-1]), 1)

