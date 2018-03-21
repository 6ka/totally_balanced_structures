import unittest
from tbs.dismantlable import DismantlableLattice
from tbs.gamma_free import GammaFree, to_string
from tbs.graph import DirectedGraph


class TestDismantlableLattice(unittest.TestCase):
    def setUp(self):
        self.lattice = DismantlableLattice(DirectedGraph.from_edges([("bottom", 1),
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
                                                                (9, "top")]))
        self.context_matrix = GammaFree.from_lattice(self.lattice)
        self.context_matrix.reorder_elements([9, 4, 3, 2, 1])
        self.context_matrix.reorder_attributes([4, 3, 7, 9, 6, 1, 5, 8])

    def test_print_boxes(self):
        string_repr = to_string(self.context_matrix)

        result = " |4 3 7 9 6 1 5 8 ⊤ " + "\n" + \
                 "-+-+-+-+-+-+-+-+-+-+" + "\n" + \
                 "9|. . .|9|-------| |" + "\n" + \
                 " +-+ +---+       |⊤|" + "\n" + \
                 "4|4|-| 7 |. . . .| |" + "\n" + \
                 " +-+-+---+-+   +---+" + "\n" + \
                 "3|||3|-*-|6|---| 8 |" + "\n" + \
                 " +|+-+---+-+ +-+---+" + "\n" + \
                 "2|| ||  7  |-|  5  |" + "\n" + \
                 " +| |+-----+-------+" + "\n" + \
                 "1|| | . | .|   1   |" + "\n" + \
                 " +-----------------+" + "\n" + \
                 "⊥|        ⊥        |" + "\n" + \
                 " +-----------------+"
        
        self.assertEqual(string_repr, result)
