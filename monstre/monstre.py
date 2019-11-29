# -*- coding: utf-8 -*-
""" Monstre """
from entity import Entity
from joueur import Joueur

SPAWN_RATE = [
    [1.0, 0.0],
    [0.75, 0.25],
    [0.0, 1.0]
]


# pylint: disable=too-few-public-methods
class Monstre(Entity):
    """ Monstre hostile aux joueurs """
    def __init__(self, carte, lig, col, vie=1):
        super(Monstre, self).__init__(lig, col, vie)
        self.carte = carte

    def update(self):
        """ Attaque une cible voisine """
        for voisin in self.carte.voisins(self.lig, self.col):
            for joueur in filter(lambda x: isinstance(x, Joueur),
                                 self.carte.entities):
                if joueur.lig == voisin[0] and joueur.col == voisin[1]:
                    self.attaquer(joueur)

    def attaquer(self, joueur):
        joueur.vie -= 1
