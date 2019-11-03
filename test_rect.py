#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from rect import Rect, intersect


class TestRect(unittest.TestCase):
    def setUp(self):
        self.rect1 = Rect(0, 0, 8, 8)
        self.rect2 = Rect(4, 4, 8, 8)

    def test_centre(self):
        x, y = self.rect1.centre()
        self.assertEqual(x, 4)
        self.assertEqual(y, 4)
        x, y = self.rect2.centre()
        self.assertEqual(x, 8)
        self.assertEqual(y, 8)

    def test_intersect(self):
        self.assertTrue(intersect(self.rect1)(self.rect2))

    def test_distance(self):
        self.assertEqual(self.rect1.distance(self.rect2), 8)

    def test_bounds(self):
        bounds = self.rect1.bounds(self.rect2)
        self.assertEqual(bounds.w, 12)
        self.assertEqual(bounds.h, 12)


if __name__ == "__main__":
    unittest.main()
