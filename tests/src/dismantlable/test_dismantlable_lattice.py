import unittest
from tbs.dismantlable_lattice import DismantlableLattice
from tbs.lattice import isa_lattice

class TestDismantlableLattice(unittest.TestCase):
    @staticmethod
    def new_lattice():
        lattice = DismantlableLattice()
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

    def test_support_tree(self):
        self.lattice.make_atomistic()
        tree = self.lattice.support_tree()
        self.assertTrue(tree.isa_edge(1, 2))
        self.assertTrue(tree.isa_edge(3, 2))
        self.assertTrue(tree.isa_edge(4, 2))
        self.assertTrue(tree.isa_edge(10, 2) or tree.isa_edge(10, 4))
        self.assertFalse(tree.isa_edge(1, 3))
        self.assertFalse(tree.isa_edge(1, 4))
        self.assertFalse(tree.isa_edge(3, 4))
        self.assertFalse(tree.isa_edge(10, 1))
        self.assertFalse(tree.isa_edge(10, 3))
        self.assertFalse(
            tree.isa_edge(10, 2) and tree.isa_edge(10, 4))

    def test_random_tb_init(self):
        random_lattice = DismantlableLattice.random_dismantlable_lattice(n_vertices=10)
        self.assertTrue(isa_lattice(random_lattice))
        self.assertEqual(len(random_lattice), 12)

    def test_from_context_matrix(self):
        matrix = [[1, 1, 0, 0],
                  [1, 1, 0, 1],
                  [0, 0, 1, 1]]

        c1 = ((0, 0), (0, 1))
        c2 = ((1, 0), (1, 1))
        c3 = ((1, 3), (1, 3))
        c4 = ((2, 2), (2, 3))

        cover_graph = DismantlableLattice()
        cover_graph.update([(c1, "TOP"),
                            (c3, "TOP"),
                            (c2, c1),
                            (c2, c3),
                            (c4, c3),
                            ("BOTTOM", c2),
                            ("BOTTOM", c4)])

        self.assertEqual(cover_graph, DismantlableLattice.from_dlo_matrix(matrix))

    def test_print_boxes(self):
        string_repr = self.lattice.print_boxes()

        result = " |4 3 7 9 6 1 5 8 " + "\n" + \
                 "-+-+-+-+-+-+-+-+-+" + "\n" + \
                 "9|. . .|9|. . . . " + "\n" + \
                 " +-+ +---+        " + "\n" + \
                 "4|4|-| 7 |. . . . " + "\n" + \
                 " +-+-+---+-+   +-+" + "\n" + \
                 "3|.|3|-*-|6|---|8|" + "\n" + \
                 " + +-+-----+ +---+" + "\n" + \
                 "2|. .|  7  |-| 5 |" + "\n" + \
                 " +   +-----+-----+" + "\n" + \
                 "1|. . . . .|  1  |" + "\n" + \
                 " +         +-----+"

        self.assertEqual(string_repr, result)



