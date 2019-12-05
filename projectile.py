#!/usr/bin/env python
# -*- coding: utf-* -*-
""" Projectile magique """

from entity import NORTH, SOUTH, EAST, WEST


# pylint: disable=too-few-public-methods
class Projectile:
    """ Projectile magique """
    def __init__(self, parent, lig, col, direction):
        self.parent = parent  # joueur ou ennemi
        self.lig = lig  # ordonnée
        self.col = col  # abscisse
        self.direction = direction  # direction de propagation

    def update(self):
        """ Mise à jour """
        if self.direction & NORTH:
            self.lig -= 1
        elif self.direction & SOUTH:
            self.lig += 1

        if self.direction & WEST:
            self.col -= 1
        elif self.direction & EAST:
            self.col += 1
