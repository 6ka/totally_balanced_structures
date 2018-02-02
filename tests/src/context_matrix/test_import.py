# -*- coding: utf-8 -*-

import unittest
import os
from tbs.contextmatrix import file_io
from tbs.contextmatrix.conversion import to_string


class TestImport(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), "../"))

    def test_load(self):
        f = open("../resources/test_table.txt")
        context_matrix = file_io.load(f)
        f.close()
        out = "   a   b   c   d \n1  X   X   X   X \n2  X   X   .   X \n3  .   X   X   X \n"
        self.assertEqual(out, to_string(context_matrix))

    def test_write_no_labels(self):
        f = open("../resources/test_table.txt")
        context_matrix = file_io.load(f)
        f.close()
        f = open("../resources/test_table_write.txt", "w")
        file_io.save(context_matrix, f, "X", "nothing_here", False, False, "+")
        f.close()
        f = open("../resources/test_table_write.txt")
        reloaded_context_matrix = file_io.load(f, False, False, lambda x: x == "X", "+")
        self.assertEqual(context_matrix.matrix, reloaded_context_matrix.matrix)
        self.assertEqual(tuple(range(4)), reloaded_context_matrix.attributes)
        self.assertEqual(tuple(range(3)), reloaded_context_matrix.elements)
        f.close()
        os.remove("../resources/test_table_write.txt")

    def test_write_labels(self):
        f = open("../resources/test_table.txt")
        context_matrix = file_io.load(f)
        f.close()
        f = open("../resources/test_table_write.txt", "w")
        file_io.save(context_matrix, f)
        f.close()
        f = open("../resources/test_table_write.txt")
        reloaded_context_matrix = file_io.load(f)
        self.assertEqual(context_matrix.matrix, reloaded_context_matrix.matrix)
        self.assertEqual(context_matrix.attributes, reloaded_context_matrix.attributes)
        self.assertEqual(context_matrix.elements, reloaded_context_matrix.elements)
        f.close()

    def test_write_elements_labels(self):
        f = open("../resources/test_table.txt")
        context_matrix = file_io.load(f)
        f.close()
        f = open("../resources/test_table_write.txt", "w")
        file_io.save(context_matrix, f, has_elements_label=False)
        f.close()
        f = open("../resources/test_table_write.txt")
        reloaded_context_matrix = file_io.load(f, has_elements_label=False)
        self.assertEqual(context_matrix.matrix, reloaded_context_matrix.matrix)
        self.assertEqual(context_matrix.attributes, reloaded_context_matrix.attributes)
        self.assertEqual(tuple(range(3)), reloaded_context_matrix.elements)
        f.close()

    def test_write_attributes_labels(self):
        f = open("../resources/test_table.txt")
        context_matrix = file_io.load(f)
        f.close()
        f = open("../resources/test_table_write.txt", "w")
        file_io.save(context_matrix, f, has_attributes_label=False)
        f.close()
        f = open("../resources/test_table_write.txt")
        reloaded_context_matrix = file_io.load(f, has_attributes_label=False)
        self.assertEqual(context_matrix.matrix, reloaded_context_matrix.matrix)
        self.assertEqual(tuple(range(4)), reloaded_context_matrix.attributes)
        self.assertEqual(context_matrix.elements, reloaded_context_matrix.elements)
        f.close()
