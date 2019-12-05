# -*- coding: utf-8 -*-
""" Rectangle """


class Rect:
    """ Rectangle 2D """
    def __init__(self, left, top, width, height, depth=0):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.depth = depth

        # précalculé car souvent utilisé
        self.point_centre = (self.left + self.width // 2,
                             self.top + self.height // 2)

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.left, self.top, self.width,
                                         self.height)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.left, self.top, self.width,
                                         self.height)

    def centre(self):
        return self.point_centre

    def bounds(self, other):
        """ Renvoie le plus petit rectangle qui contienne :self: et :other: """
        return Rect(
            min(self.left, other.left), min(self.top, other.top),
            self.width + other.width + other.left - self.left - self.width,
            self.height + other.height + other.top - self.top - self.height)

    def contains(self, x_point, y_point):
        """ Renvoie True si le point (:x_point:, :y_point:) appartient au rectangle """
        return self.left <= x_point <= self.left + self.width and self.top <= y_point <= self.top + self.height


def intersect(s1):
    return lambda s2: s1.x - 1 < s2.x + s2.w + 1 and s2.x - 1 < s1.x + s1.w + 1 and s1.y - 1 < s2.y + s2.h + 1 and s2.y - 1 < s1.y + s1.h + 1


def distance(lig1, col1, lig2, col2):
    """ Renvoie la distance entre deux cellules """
    return abs(lig2 - lig1) + abs(col2 - col1)
