# -*- coding: utf-8 -*-

import unittest

import os
import sys
sys.path.append(os.path.dirname('../DLC/'))

test_loader = unittest.TestLoader()
all_suites = unittest.TestSuite()

for suite in test_loader.discover("src/", "test_*.py"):
    all_suites.addTests(suite)

unittest.TextTestRunner(verbosity=2).run(all_suites)