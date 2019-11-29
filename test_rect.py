#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tests sur les rectangles """
import unittest

from rect import Rect


class TestRect(unittest.TestCase):
    """ Tests sur les rectangles """
    def setUp(self):
        """ Crée deux rectangles """
        self.rect1 = Rect(0, 0, 8, 8)
        self.rect2 = Rect(4, 4, 8, 8)

    def test_centre(self):
        """ Vérifie les coordonées du centre """
        x_centre, y_centre = self.rect1.centre()
        self.assertEqual(x_centre, 4)
        self.assertEqual(y_centre, 4)

        x_centre, y_centre = self.rect2.centre()
        self.assertEqual(x_centre, 8)
        self.assertEqual(y_centre, 8)

    def test_bounds(self):
        """ Vérife le plus petit conteneur commun """
        bounds = self.rect1.bounds(self.rect2)
        self.assertEqual(bounds.width, 12)
        self.assertEqual(bounds.height, 12)


if __name__ == "__main__":
    unittest.main()
