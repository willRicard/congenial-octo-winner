# -*- coding: utf-8 -*-
""" Monstre """
from entity import Entity, a_etoile, distance

from joueur import Joueur

THRESHOLD_DISTANCE = 20


# pylint: disable=too-few-public-methods
class Monstre(Entity):
    """ Monstre hostile aux joueurs """
    def __init__(self, carte, lig, col, vie=1):
        super(Monstre, self).__init__(lig, col, vie)
        self.carte = carte

        self.moved = False

    def update(self):
        """ Déplacement vers la cible """
        if self.moved:
            self.moved = False
            return

        start = (self.lig, self.col)
        for entity in self.carte.entities:
            if isinstance(entity, Joueur) and distance(
                    *start, entity.lig, entity.col) <= THRESHOLD_DISTANCE:
                goal = (entity.lig, entity.col)
                path = a_etoile(self.carte, start, goal)
                prochain = path[0]

                self.lig = prochain[0]
                self.col = prochain[1]
                self.moved = True
