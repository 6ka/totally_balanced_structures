import unittest

from tbs.graph import DirectedGraph

from tbs.lattice import isa_lattice_directed_comparability_graph
from tbs.dismantlable import DismantlableLattice


class TestLatticeBinarize(unittest.TestCase):
    def setUp(self):
        self.hase_diagram = DirectedGraph.from_edges([("bottom", 1),
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
        self.lattice = DismantlableLattice(self.hase_diagram)

    def test_is_binary(self):
        self.assertFalse(self.lattice.is_binary())
        lattice = DismantlableLattice(DirectedGraph.from_edges([("bottom", 1),
                                                                ("bottom", 3),
                                                                ("bottom", 4),
                                                                (1, 5),
                                                                (3, 6),
                                                                (4, 7),
                                                                (5, 8),
                                                                (6, 8),
                                                                (7, 9),
                                                                (8, "top"),
                                                                (9, "top")]))

        self.assertTrue(lattice.is_binary())

    def test_element_is_binary(self):
        self.assertTrue(self.lattice.isa_binary_element(5))
        self.assertTrue(self.lattice.isa_binary_element(6))
        self.assertTrue(self.lattice.isa_binary_element(4))
        self.assertFalse(self.lattice.isa_binary_element(2))
        self.assertFalse(self.lattice.isa_binary_element("bottom"))

    def test_bottom_up_element_binarization(self):
        self.lattice.binarization_element_above(2, lambda lattice, x, y: len(lattice) - 1)
        self.assertLessEqual(len(self.lattice.above(2)), 2)
        self.assertNotIn(7, self.lattice.above(10))
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_bottom_up_element_four_above_binarization(self):
        new_hase_diagram = self.hase_diagram.update(((2, 10),(10, "top")))
        new_lattice = DismantlableLattice(new_hase_diagram)
        new_lattice.binarization_element_above(2, lambda lattice, x, y: len(lattice) - 1)
        self.assertLessEqual(len(new_lattice.above(2)), 2)
        self.assertTrue(isa_lattice_directed_comparability_graph(new_hase_diagram))

    def test_top_down_element_four_under_binarization(self):
        new_hase_diagram = self.hase_diagram.update((("bottom", 10), (10, "top"), ("bottom", 11), (11, "top")))
        new_lattice = DismantlableLattice(new_hase_diagram)
        new_lattice.binarization_element_under("top", lambda lattice, x, y: len(lattice) - 1)
        self.assertLessEqual(len(new_lattice.under("top")), 2)
        self.assertTrue(isa_lattice_directed_comparability_graph(new_hase_diagram))

    def test_bottom_up_binary_element_binarization(self):
        self.lattice.binarization_element_above(5)
        self.assertLessEqual(len(self.lattice.above(2)), 5)
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_top_down_element_binarization(self):
        self.hase_diagram.update((('bottom', 10), (10, 7), (10, 11), (11, 'top')))
        self.lattice = DismantlableLattice(self.hase_diagram)
        self.lattice.binarize_element(7)
        self.assertTrue(self.lattice.isa_binary_element(7))
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_binarize_element(self):

        self.hase_diagram.difference([('bottom', 2)])
        self.hase_diagram.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2)))
        self.lattice = DismantlableLattice(self.hase_diagram)
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

        self.lattice.binarize_element(2)
        self.assertTrue(self.lattice.isa_binary_element(2))
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_binarize_binary_element(self):
        self.lattice.binarize_element(5)
        self.assertTrue(self.lattice.isa_binary_element(5))
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_binarize_with_one_element_bottom_up_not_binary(self):
        self.lattice.binarize()
        self.assertTrue(self.lattice.is_binary())
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_binarize_with_one_element_not_binary(self):
        self.hase_diagram.difference([('bottom', 2)])
        self.hase_diagram.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2)))
        self.lattice = DismantlableLattice(self.hase_diagram)

        self.lattice.binarize()
        self.assertTrue(self.lattice.is_binary())
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_binarize(self):
        self.lattice.binarize()
        self.assertTrue(self.lattice.is_binary())
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))

    def test_binarize_with_ignored_elements(self):
        self.lattice.binarize({2})
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))
        self.assertFalse(self.lattice.isa_binary_element(2))
        for element in self.lattice:
            if element != 2 and element != 'bottom':
                self.assertTrue(self.lattice.isa_binary_element(element))

    def test_bottom_up_binarization(self):
        self.lattice.binarize_bottom_up()
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))
        for element in self.lattice:
            if element != 'bottom':
                self.assertTrue(len(self.lattice.above(element)) <= 2)

    def test_bottom_up_binarization_with_ignored_elements(self):
        self.lattice.binarize_bottom_up({2})
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))
        self.assertFalse(len(self.lattice.above(2)) <= 2)
        for element in self.lattice:
            if element != 2 and element != 'bottom':
                self.assertTrue(len(self.lattice.above(element)) <= 2)

    def test_top_down_binarization(self):
        self.hase_diagram.difference([('bottom', 4)])
        self.hase_diagram.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 4), (11, 4), (12, 4)))
        self.lattice = DismantlableLattice(self.hase_diagram)

        self.lattice.binarize_top_down()
        self.assertTrue(isa_lattice_directed_comparability_graph(self.lattice.hase_diagram))
        for element in self.lattice:
            self.assertTrue(len(self.lattice.under(element)) <= 2)
        self.assertTrue(len(self.lattice.above(2)) > 2)

    def test_other_successor(self):
        self.hase_diagram.difference(((2, 7),))
        self.lattice = DismantlableLattice(self.hase_diagram)

        self.assertEqual(self.lattice.other_above(2, 5), 6)

    def test_atomistic_contraction_order(self):
        self.hase_diagram.difference([(2, 5), (2, 6)])
        self.hase_diagram.update(((2, 11), (11, 5), (11, 6)))  # binarize
        self.hase_diagram.update((('bottom', 10), (10, 9), ('bottom', 12), (12, 11)))  # transforms objects into atoms
        self.lattice = DismantlableLattice(self.hase_diagram)

        order = self.lattice.decomposition_order()
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
        order = self.lattice.decomposition_order()
        self.assertTrue(order.index(8) > order.index(5))
        self.assertTrue(order.index(8) > order.index(6))
        self.assertTrue(order.index(9) > order.index(7))

    def test_contraction_order_with_red_path(self):
        binary_atomistic_lattice = DismantlableLattice(DirectedGraph.from_edges(
            (('BOTTOM', 3), ('BOTTOM', 10), ('BOTTOM', 11), ('BOTTOM', 12), ('BOTTOM', 13),
             ('BOTTOM', 14), ('BOTTOM', 15), (0, 9), (1, 5), (1, 8), (2, 'TOP'), (3, 1),
             (3, 4), (4, 2), (5, 'TOP'), (6, 9), (8, 0), (8, 6), (9, 2), (10, 0), (11, 1),
             (12, 4), (13, 5), (14, 6), (15, 8))))

        order = binary_atomistic_lattice.decomposition_order()
        for i in [0, 2, 5, 6, 8, 9]:
            self.assertTrue(order.index(1) < order.index(i))
            self.assertTrue(order.index(4) < order.index(i))
        self.assertTrue(order.index(6) > order.index(5))
        self.assertTrue(order.index(0) > order.index(5))
