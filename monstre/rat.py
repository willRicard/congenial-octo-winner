# -*- coding: utf-8 -*-
from random import choice

from monstre.monstre import Monstre

from entity import NORTH, WEST, EAST, SOUTH


class Rat(Monstre):
    def __init__(self, carte, lig, col):
        super(Rat, self).__init__(carte, lig, col, 1)
        self.moved = False

    def update(self):
        if self.moved:
            self.moved = False
            return

        self.deplacer(self.carte, choice((NORTH, WEST, EAST, SOUTH)))
        self.moved = True
