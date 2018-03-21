import unittest
from tbs.dismantlable import random_dismantlable_lattice
from tbs.lattice import isa_lattice_directed_comparability_graph


class TestDismantlableLattice(unittest.TestCase):
    def test_random_tb_init(self):
        random_lattice = random_dismantlable_lattice(n_vertices=10)
        self.assertTrue(isa_lattice_directed_comparability_graph(random_lattice.hase_diagram))
        self.assertEqual({"BOTTOM", "TOP", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, set(random_lattice))

