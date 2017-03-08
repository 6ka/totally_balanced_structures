import unittest
from TBS.graph import Graph
from TBS.binarize import atoms, coatoms, smaller_atoms, max_intersection, is_binary, element_is_binary, \
    bottom_up_element_binarization, binarize_element
from TBS.lattice import comparability_function, dual_lattice, isa_lattice


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
        assert atoms(self.lattice) == {1, 2, 3, 4}

    def test_coatoms(self):
        assert coatoms(self.lattice) == {8, 9}

    def test_smaller_atoms(self):
        smaller_than = comparability_function(self.lattice)
        assert smaller_atoms({1, 2, 3, 4}, 8, smaller_than) == {1, 2, 3}
        assert smaller_atoms({1, 2, 3, 4}, "top", smaller_than) == {1, 2, 3, 4}
        assert smaller_atoms({1, 2, 3, 4}, 9, smaller_than) == {2, 4}

    def test_max_intersection(self):
        antichain = [{0, 1, 2, 3}, {6, 7}, {3, 4, 5, 6}, {2, 3, 4, 8, 9}, {9, 10}]
        for i in range(5):
            max_inter = max_intersection(antichain)
            assert max_inter in {(0, 3), (3, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)}

    def test_max_intersection_with_equality(self):
        antichain = [{0, 1}, {0, 1}, {0, 2}]
        for i in range(5):
            max_inter = max_intersection(antichain)
            assert max_inter in {(0, 1), (1, 0)}

    def test_is_binary(self):
        assert not is_binary(self.lattice)
        assert is_binary(self.lattice.restriction(["bottom", 2, 3, 5, 6, 8]))

    def test_element_is_binary(self):
        assert element_is_binary(self.lattice, self.dual_lattice, 5)
        assert element_is_binary(self.lattice, self.dual_lattice, 6)
        assert element_is_binary(self.lattice, self.dual_lattice, 4)
        assert not element_is_binary(self.lattice, self.dual_lattice, 2)
        assert not element_is_binary(self.lattice, self.dual_lattice, "bottom")

    def test_one_direction_binarize_element(self):
        binarized_2_lattice = bottom_up_element_binarization(self.lattice, 2)
        assert len(binarized_2_lattice[2]) <= 2
        assert binarized_2_lattice[2] == [10, 7]
        assert isa_lattice(binarized_2_lattice)

    def test_one_direction_binarize_binary_element(self):
        binarized_5_lattice = bottom_up_element_binarization(self.lattice, 5)
        assert len(binarized_5_lattice[2]) <= 5
        assert isa_lattice(binarized_5_lattice)

    def test_binarize_element_other_direction(self):
        self.lattice.update((('bottom', 10), (10, 7), (10, 11), (11, 'top')))
        binarized_7_lattice = binarize_element(self.lattice, 7)
        assert element_is_binary(binarized_7_lattice, dual_lattice(binarized_7_lattice), 7)
        assert isa_lattice(binarized_7_lattice)

    def test_binarize_element(self):
        self.lattice.update((('bottom', 10), ('bottom', 11), ('bottom', 12), (10, 2), (11, 2), (12, 2), ('bottom', 2)))
        binarized_2_lattice = binarize_element(self.lattice, 2)
        assert element_is_binary(binarized_2_lattice, dual_lattice(binarized_2_lattice), 2)
        assert binarized_2_lattice[2] == [13, 7]
        assert isa_lattice(binarized_2_lattice)

    def test_binarize_binary_element(self):
        binarized_5_lattice = binarize_element(self.lattice, 5)
        assert element_is_binary(binarized_5_lattice, dual_lattice(binarized_5_lattice), 5)
        assert isa_lattice(binarized_5_lattice)
