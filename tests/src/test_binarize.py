import unittest
from TBS.graph import Graph
from TBS.binarize import max_intersection, is_binary, element_is_binary, bottom_up_element_binarization, \
    binarize_element, binarize, bottom_up_binarization, top_down_binarization, bfs_binarization, \
    move_sup_irreducibles_to_atoms, atoms, flat_contraction_order, is_flat, contraction_order
from TBS.lattice import dual_lattice, isa_lattice
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
        self.assertListEqual(atoms(self.lattice), [1, 2, 3, 4])
        self.assertListEqual(atoms(self.lattice, "bottom"), [1, 2, 3, 4])

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
        self.assertListEqual(atoms(flat_lattice), [1, 2, 3, 4, 10])
        self.assertListEqual(flat_lattice[10], [9])

    def test_flat_contraction_order(self):
        self.lattice.update((('bottom', 10), (10, 9)))  # transforms objects into atoms
        self.lattice.update(((2, 5), (2, 6), (2, 11), (11, 5), (11, 6)))  # binarize
        order = flat_contraction_order(self.lattice)
        self.assertTrue(order.index(8) > order.index(5))
        self.assertTrue(order.index(8) > order.index(6))
        self.assertTrue(order.index(5) > order.index(1))
        self.assertTrue(order.index(5) > order.index(11))
        self.assertTrue(order.index(6) > order.index(11))
        self.assertTrue(order.index(6) > order.index(3))
        self.assertTrue(order.index(7) > order.index(2))
        self.assertTrue(order.index(7) > order.index(4))
        self.assertTrue(order.index(9) > order.index(7))
        self.assertTrue(order.index(9) > order.index(10))

    def test_is_flat(self):
        self.assertFalse(is_flat(self.lattice))
        self.lattice.update((('bottom', 10), (10, 9)))
        self.assertTrue(is_flat(self.lattice))
        self.assertTrue(is_flat(self.lattice, "bottom"))

    def test_contraction_order(self):
        order = contraction_order(self.lattice)
        self.assertTrue(order.index(8) > order.index(5))
        self.assertTrue(order.index(8) > order.index(6))
        self.assertTrue(order.index(5) > order.index(1))
        self.assertTrue(order.index(5) > order.index(2))
        self.assertTrue(order.index(6) > order.index(2))
        self.assertTrue(order.index(6) > order.index(3))
        self.assertTrue(order.index(7) > order.index(2))
        self.assertTrue(order.index(7) > order.index(4))
        self.assertTrue(order.index(9) > order.index(7))