# -*- coding: utf-8 -*-
""" Joueur """
from random import random

from entity import Entity, ALIMENT_POISON, ALIMENT_CURSE

## Points de vie max d'un joeur de niveau 1
BASE_VIE = 100
## Points de magie max d'un joueur de niveau 1
BASE_MANA = 100

## Probabilité de guérison spontanée d'un joueur empoisonné/maudit
PROBA_RECOVER = 0.02


class Joueur(Entity):
    """ Joueur représenté par un @ """
    def __init__(self, lig, col):
        """ Constructeur """
        super(Joueur, self).__init__(lig, col, vie=BASE_VIE)

        ## Points de magie
        self.mana = BASE_MANA
        ## Points de magie max
        self.max_mana = BASE_MANA

        ## Niveau
        self.level = 1
        ## Expérience
        self.exp = 0

    def update(self):
        """ Met a jour l'etat du joueur suivant ses altérations d'état. """
        if self.mana < self.max_mana:
            self.mana += 0.5
        if self.aliment & ALIMENT_POISON and random() < 0.2:
            self.vie -= 1
        if self.aliment & ALIMENT_CURSE and self.mana > 0 and random() < 0.2:
            self.mana -= 1

        if random() < PROBA_RECOVER:
            self.aliment &= 0

    def level_up(self):
        """ Améliore les attributs du joueur """
        self.max_vie += self.level
        self.vie = self.vie

        self.max_mana += self.level
        self.mana = self.max_mana

    def shoot(self, carte):
        """ Tire un projectile devant le joueur. """
        if self.mana > 0:
            self.mana -= 1
            carte.ajouter_projectile(self)
