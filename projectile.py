#!/usr/bin/env python
# -*- coding: utf-* -*-
""" Projectile magique """

from joueur import NORTH, SOUTH, EAST, WEST


# pylint: disable=too-few-public-methods
class Projectile:
    """ Projectile magique """
    def __init__(self, parent, lig, col, direction):
        self.parent = parent
        self.lig = lig
        self.col = col
        self.direction = direction

    def update(self):
        """ Mise à jour """
        if self.direction == NORTH:
            self.lig -= 1
        elif self.direction == SOUTH:
            self.lig += 1
        elif self.direction == WEST:
            self.col -= 1
        elif self.direction == EAST:
            self.col += 1
