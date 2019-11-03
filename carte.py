#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tableau 2D de caractères """
import curses
from random import random, randrange, choice

from rect import Rect, intersect

from config import NORTH, SOUTH, EAST, WEST, NUM_SALLES, EPAISSEUR_MUR, POISON, CURSE

from util import dialog


class Carte:
    """ Une carte de caractères """

    def __init__(self, hauteur=100, largeur=100):
        self.hauteur = hauteur
        self.largeur = largeur

        self.pad = curses.newpad(hauteur + 1, largeur + 1)
        self.lig_scroll = 0
        self.col_scroll = 0

        self.cases = [['#'] * largeur for lig in range(hauteur)]
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
                self.cases[lig][col] = '.'
        else:
            lig = depart[1]
            for col in range(min(depart[0], arrivee[0]),
                             max(depart[0], arrivee[0]) + 1):
                self.cases[lig][col] = '.'

    def generer_salles(self):
        """ Genere des salles aleatoires """
        largeur_max = self.largeur // 3
        hauteur_max = self.hauteur // 3

        salles = []
        num_iter = 0
        while len(salles) < NUM_SALLES and num_iter < 100:
            num_iter += 1
            x = randrange(0, self.largeur - largeur_max)
            y = randrange(0, self.hauteur - hauteur_max)
            w = randrange(8, largeur_max)
            h = randrange(8, hauteur_max)

            candidat = Rect(x, y, w, h)

            if not any(map(intersect(candidat), salles)):
                salles.append(Rect(x, y, w, h))

        for salle in salles:
            for lig in range(salle.y, salle.y + salle.h):
                for col in range(salle.x, salle.x + salle.w):
                    self.cases[lig][col] = '.'

        conn = [[False for _ in range(NUM_SALLES)] for _ in range(NUM_SALLES)]
        salle = salles[0]
        for i, salle in enumerate(salles):
            proche = min(
                filter(
                    lambda s: id(s) != id(salle) and not conn[i][salles.index(
                        salle)],  # autres salles non connectees
                    salles),
                key=salle.distance)
            j = salles.index(proche)
            conn[i][j] = conn[j][i] = True

            bounds = salle.bounds(proche)

            milieu = bounds.centre()

            milieu_dans = intersect(Rect(*milieu, 1, 1))

            if milieu_dans(salle):
                self.relier(milieu, proche.centre())
            elif milieu_dans(proche):
                self.relier(milieu, salle.centre())
            else:  # couloir en forme de 'L'
                carrefour = (salle.centre()[0], proche.centre()[1])
                self.relier(salle.centre(), carrefour)
                self.relier(carrefour, proche.centre())

        self.salles = salles

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
            if random() > 0.4:
                self.partitionner(enfant)
            # pas de salle
            elif random() < 0.2:
                enfants.remove(enfant)
            # grande salle
            else:
                self.salles.append(enfant)

        for enfant in enfants:
            self.relier(salle.centre(), enfant.centre())
            autre = choice(enfants)
            oops = 0
            while autre == enfant and oops <= 1000:
                autre = choice(enfants)
                oops += 1
            self.relier(enfant.centre(), autre.centre())

        return enfants

    def generer_salles_partitionnement(self):
        """ Genere les salles par une approche récursive """
        # on laisse un mur autour du donjon
        donjon = Rect(1, 1, self.largeur - 2, self.hauteur - 2)

        self.partitionner(donjon)

        for i, salle in enumerate(self.salles):
            for lig in range(salle.y, salle.y + salle.h):
                for col in range(salle.x, salle.x + salle.w):
                    self.cases[lig][col] = '.'

    def affiche(self):
        """ Affiche la carte sur un écran ncurses :scr: """
        for lig in range(self.hauteur):
            for col in range(self.largeur):
                attr = curses.A_NORMAL
                if self.cases[lig][col] == '#':
                    attr = curses.A_REVERSE
                if self.cases[lig][col] == '❇︎':
                    attr = curses.color_pair(2)
                self.pad.addstr(lig, col, self.cases[lig][col], attr)

    def update(self, joueur):
        """ Affiche le joueur, les monstres et les projectiles """
        # Scrolling
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= curses.LINES - 2 and self.lig_scroll <= self.hauteur - curses.LINES:
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll -= 1
        elif joueur.col - self.col_scroll >= curses.COLS - 2 and self.col_scroll <= self.largeur - curses.COLS:
            self.col_scroll += 1

        joueur.affiche(self.pad)

        # Projectiles
        for projectile in self.projectiles:
            lig, col, direction = projectile
            self.cases[lig][col] = '.'
            if direction == NORTH:
                projectile[0] -= 1
            elif direction == SOUTH:
                projectile[0] += 1
            elif direction == WEST:
                projectile[1] += 1
            elif direction == EAST:
                projectile[1] -= 1
            lig, col, direction = projectile
            if self.case_libre(lig, col):
                self.cases[lig][col] = '❇︎'
            else:
                self.projectiles.remove(projectile)

        # On laisse la derinière ligne pour l'ITH
        self.pad.refresh(self.lig_scroll, self.col_scroll, 0, 0,
                         curses.LINES - 2, curses.COLS - 1)

    def case_libre(self, lig, col):
        """ Renvoie True si la case est libre (ni mur, ni monstre) """
        return 0 <= lig <= self.hauteur and 0 <= col <= self.largeur and self.cases[
            lig][col] != '#'
