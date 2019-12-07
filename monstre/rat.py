# -*- coding: utf-8 -*-
""" Rat """
from random import random, choice

from monstre.monstre import Monstre

from entity import NORTH, WEST, EAST, SOUTH, ALIMENT_POISON

from joueur import Joueur

## Probabilité d'empoisonnement du joueur par morsure
PROBA_POISON = 0.5


class Rat(Monstre):
    """ Monstre simple
    Le rat se déplace un tour sur deux dans une direction aléatoire
    Une morsure peut empoisonner le joueur """
    def __init__(self, carte, lig, col):
        """ Constructeur """
        super(Rat, self).__init__(carte, lig, col, 1)
        ## Indique si le rat a bougé au dernier tour
        self.moved = False

    def update(self):
        """ Déplacement aléatoire """
        if self.moved:
            self.moved = False
            return

        self.deplacer(self.carte, choice((NORTH, WEST, EAST, SOUTH)))
        self.moved = True

        for entity in self.carte.entities:
            if isinstance(
                    entity, Joueur
            ) and self.lig == entity.lig and self.col == entity.col:
                self.attaquer(entity)

    def attaquer(self, joueur):
        """ La morsure du rat peut empoisonner le joueur """
        joueur.vie -= 1
        if random() < PROBA_POISON:
            joueur.aliment |= ALIMENT_POISON
