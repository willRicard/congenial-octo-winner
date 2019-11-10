# -*- coding: utf-8 -*-
""" Rectangle """


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # précalculé car souvent utilisé
        self.point_centre = (self.x + self.w // 2, self.y + self.h // 2)

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.x, self.y, self.w, self.h)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.x, self.y, self.w, self.h)

    def centre(self):
        # return (self.x + self.w // 2, self.y + self.h // 2)
        return self.point_centre

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.x - other.y)

    def bounds(self, other):
        """ Renvoie le plus petit rectangle qui contienne :self: et :other: """
        return Rect(min(self.x, other.x), min(self.y, other.y),
                    self.w + other.w + other.x - self.x - self.w,
                    self.h + other.h + other.y - self.y - self.h)


def intersect(s1):
    return lambda s2: s1.x - 1 < s2.x + s2.w + 1 and s2.x - 1 < s1.x + s1.w + 1 and s1.y - 1 < s2.y + s2.h + 1 and s2.y - 1 < s1.y + s1.h + 1
