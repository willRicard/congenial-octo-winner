#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tests sur la carte """

import unittest

from carte import Carte


class TestCarte(unittest.TestCase):
    """ Tests sur la carte """
    def test_relier(self):
        """ Teste la création de couloirs """
        carte = Carte(4, 4)
        carte.relier((0, 0), (3, 0))
        carte.relier((0, 0), (0, 3))
        carte.relier((3, 0), (3, 3))
        self.assertListEqual(carte.cases,
                             [['.', '.', '.', '.'], ['.', '#', '#', '.'],
                              ['.', '#', '#', '.'], ['.', '#', '#', '.']])

    def test_voisins(self):
        """ Teste la détection de voisins """
        carte = Carte(4, 4)
        for lig in range(4):
            for col in range(4):
                carte.cases[lig][col] = '.'

        voisins = list(carte.voisins(0, 0))
        self.assertEqual(len(voisins), 2)

        voisins = list(carte.voisins(1, 1))
        self.assertEqual(len(voisins), 4)


if __name__ == "__main__":
    unittest.main()
