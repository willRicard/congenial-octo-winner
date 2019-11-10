# -*- coding: utf-8 -*-
""" Joueur et Interface Tête Haute (ITH) """

import curses
from gettext import gettext

NORTH = 1
SOUTH = 2
WEST = 4
EAST = 8

BASE_VIE = 100
BASE_MANA = 100
BASE_GOLD = 10

POISON = 1
CURSE = 2


class Joueur():
    """ Joueur représenté par un @ """
    def __init__(self, lig, col):
        self.lig = lig
        self.col = col
        self.facing = NORTH

        self.vie = self.max_vie = BASE_VIE

        self.mana = self.max_mana = BASE_MANA

        self.level = 1
        self.exp = 0
        self.gold = BASE_GOLD
        self.aliment = 0

    def update(self):
        """ Met a jour l'etat du joueur suivant ses altérations d'état. """
        from random import random
        if self.aliment & POISON and random() < 0.2:
            self.vie -= 1
        if self.aliment & CURSE and self.mana > 0 and random() < 0.2:
            self.mana -= 1

    def affiche(self, scr):
        """ Affiche le joueur """
    def level_up(self):
        """ Augmente les attributs du joueur """
        self.max_vie += self.level
        self.vie = self.vie

        self.max_mana += self.level
        self.mana = self.max_mana

    def shoot(self, carte):
        """ Tire un projectile devant le joueur. """
        if self.mana > 0:
            self.mana -= 1
            carte.ajouter_projectile(self.lig, self.col, self.facing)
