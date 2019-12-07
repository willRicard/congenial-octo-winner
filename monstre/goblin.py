# -*- coding: utf-8 -*-
""" Monstre """
from entity import a_etoile, distance
from joueur import Joueur

from monstre.monstre import Monstre

## Distance seuil pour abandonner la poursuite du joueur
THRESHOLD_DISTANCE = 20


# pylint: disable=too-few-public-methods
class Goblin(Monstre):
    """ Le goblin se déplace intelligemment vers le joueur """
    def __init__(self, carte, lig, col, vie=1):
        """ Constructeur """
        super(Goblin, self).__init__(lig, col, vie)
        ## Conservé pour A*
        self.carte = carte

    def update(self):
        """ Déplacement vers la cible """
        super(Goblin, self).update()

        start = (self.lig, self.col)
        for entity in self.carte.entities:
            if isinstance(entity, Joueur) and distance(
                    *start, entity.lig, entity.col) <= THRESHOLD_DISTANCE:
                goal = (entity.lig, entity.col)
                path = a_etoile(self.carte, start, goal)
                prochain = path[0]

                if prochain != goal:
                    self.lig = prochain[0]
                    self.col = prochain[1]

    def attaquer(self, joueur):
        """Le goblin n'est pas très fort et enlève au :joueur: un
        seul point de vie """
        joueur.vie -= 1
