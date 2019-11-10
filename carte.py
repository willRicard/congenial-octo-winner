# -*- coding: utf-8 -*-
""" Tableau 2D de caractères """
from random import random, randrange, choice

from rect import Rect, intersect
from joueur import NORTH, SOUTH, WEST, EAST

NUM_SALLES = 10
PROBA_ARRET = 0.2
PROBA_GRANDE_SALLE = 0.2
EPAISSEUR_MUR = 1

SYMBOLE_JOUEUR = '@'
SYMBOLE_PROJECTILE = '*'
SYMBOLE_SOL = '.'
SYMBOLE_MUR = '#'
SYMBOLE_MONSTRE = 'X'


class Carte:
    """ Une carte de caractères """
    def __init__(self, hauteur=100, largeur=100):
        self.hauteur = hauteur
        self.largeur = largeur

        self.lig_scroll = 0
        self.col_scroll = 0

        self.cases = [[SYMBOLE_MUR] * largeur for lig in range(hauteur)]
        self.visible = [[False] * largeur for lig in range(hauteur)]

        self.salles = []

        self.projectiles = []

    def relier(self, depart, arrivee):
        """ Couloir entre :depart: et :arrivee: """
        vertical = (depart[0] == arrivee[0])
        if vertical:
            col = depart[0]
            for lig in range(min(depart[1], arrivee[1]),
                             max(depart[1], arrivee[1]) + 1):
                self.cases[lig][col] = SYMBOLE_SOL
        else:
            lig = depart[1]
            for col in range(min(depart[0], arrivee[0]),
                             max(depart[0], arrivee[0]) + 1):
                self.cases[lig][col] = '.'

    def partitionner(self, salle):
        # Condition d'arrêt: arrêt aléatoire ou salle trop petite
        if salle.w <= 10 or salle.h <= 10:
            self.salles.append(salle)
            return

        w_max = salle.w // 3
        h_max = salle.h // 3
        x_split = randrange(w_max, salle.w - w_max)
        y_split = randrange(h_max, salle.h - h_max)

        enfants = [
            # Haut gauche
            Rect(salle.x, salle.y, x_split, y_split),
            # Haut droite
            Rect(salle.x + x_split + EPAISSEUR_MUR, salle.y,
                 salle.w - x_split - 2 * EPAISSEUR_MUR, y_split),
            # Bas gauche
            Rect(salle.x, salle.y + y_split + EPAISSEUR_MUR, x_split,
                 salle.h - y_split - 2 * EPAISSEUR_MUR),
            # Bas droite
            Rect(salle.x + x_split + EPAISSEUR_MUR,
                 salle.y + y_split + EPAISSEUR_MUR,
                 salle.w - x_split - 2 * EPAISSEUR_MUR,
                 salle.h - y_split - 2 * EPAISSEUR_MUR)
        ]

        # on copie pour enlever
        # des éléments sans
        # casser la boucle
        for enfant in list(enfants):
            # profondeur suivante
            if random() > PROBA_ARRET + PROBA_GRANDE_SALLE:
                self.partitionner(enfant)
            # pas de salle
            elif random() < PROBA_ARRET:
                enfants.remove(enfant)
            # grande salle
            else:
                self.salles.append(enfant)

        # On relie les salles
        # pour qu'elles soient
        # toutes atteignables
        for enfant in enfants:
            self.relier(salle.centre(),
                        enfant.centre())  # on relie chaque salle à son parent
            autre = choice(enfants)
            oops = 0
            while autre == enfant and oops <= 1000:
                autre = choice(enfants)
                oops += 1
            self.relier(enfant.centre(), autre.centre())

        return enfants

    def generer_salles(self):
        """ Genere les salles par une approche récursive """
        # on laisse un mur autour du donjon
        donjon = Rect(1, 1, self.largeur - 2, self.hauteur - 2)

        self.partitionner(donjon)

        for i, salle in enumerate(self.salles):
            for lig in range(salle.y, salle.y + salle.h):
                for col in range(salle.x, salle.x + salle.w):
                    self.cases[lig][col] = SYMBOLE_SOL

    def ajouter_projectile(self, lig, col, direction):
        """ Ajoute un projectile aux coordonnées :lig: :col: se déplaçant dans la :direction:
            Rien ne se passe si la case est occupée. """
        if self.case_libre(lig, col):
            self.projectiles.append([lig, col, direction])
            self.cases[lig][col] = SYMBOLE_PROJECTILE

    def update(self, joueur):
        """ Affiche le joueur, les monstres et les projectiles """
        # Projectiles
        for projectile in self.projectiles:
            lig, col, direction = projectile
            self.cases[lig][col] = '.'
            if direction == NORTH:
                projectile[0] -= 1
            elif direction == SOUTH:
                projectile[0] += 1
            elif direction == WEST:
                projectile[1] -= 1
            elif direction == EAST:
                projectile[1] += 1
            lig, col, direction = projectile
            if self.case_libre(lig, col):
                self.cases[lig][col] = SYMBOLE_PROJECTILE
            else:
                self.projectiles.remove(projectile)

    def case_libre(self, lig, col):
        """ Renvoie True si la case est libre (ni mur, ni monstre) """
        return 0 <= lig <= self.hauteur and 0 <= col <= self.largeur and self.cases[
            lig][col] != SYMBOLE_MUR
