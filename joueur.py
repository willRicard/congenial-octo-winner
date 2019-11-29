# -*- coding: utf-8 -*-
""" Joueur """
from random import random

from entity import Entity

BASE_VIE = 100
BASE_MANA = 100

# @enum Altération d'état
ALIMENT_POISON = 1
ALIMENT_CURSE = 2


class Joueur(Entity):
    """ Joueur représenté par un @ """

    def __init__(self, lig, col):
        super(Joueur, self).__init__(lig, col, vie=BASE_VIE)

        self.mana = self.max_mana = BASE_MANA

        self.level = 1
        self.exp = 0

    def update(self):
        """ Met a jour l'etat du joueur suivant ses altérations d'état. """
        if self.aliment & ALIMENT_POISON and random() < 0.2:
            self.vie -= 1
        if self.aliment & ALIMENT_CURSE and self.mana > 0 and random() < 0.2:
            self.mana -= 1

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
            carte.ajouter_projectile(self)
