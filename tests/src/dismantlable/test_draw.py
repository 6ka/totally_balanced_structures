import unittest
from tbs.dismantlable import DismantlableLattice
from tbs.graph import DirectedGraph


class TestDismantlableLattice(unittest.TestCase):
    @staticmethod
    def new_lattice():
        lattice = DismantlableLattice(DirectedGraph().update([("bottom", 1),
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
        return lattice

    def setUp(self):
        self.lattice = self.new_lattice()

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
