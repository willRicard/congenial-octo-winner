#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import curses

from carte import Carte


class TestCarte(unittest.TestCase):
    def setUp(self):
        self.carte = Carte(4, 4)

    def test_relier(self):
        self.carte.relier((0, 0), (3, 0))
        self.carte.relier((0, 0), (0, 3))
        self.carte.relier((3, 0), (3, 3))
        self.assertListEqual(self.carte.cases,
                             [['.', '.', '.', '.'], ['.', '#', '#', '#'],
                              ['.', '#', '#', '#'], ['.', '.', '.', '.']])


if __name__ == "__main__":
    curses.initscr()
    unittest.main()
