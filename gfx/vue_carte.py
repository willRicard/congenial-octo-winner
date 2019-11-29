# -*- coding: utf-8 -*-
""" Affichage de la carte """
import sys

import pygame as pg

from carte import SYMBOLE_MUR, SYMBOLE_PROJECTILE
from joueur import ALIMENT_POISON, ALIMENT_CURSE

from monstre.rat import Rat
from monstre.monstre import Monstre

TILE_SIZE = 16

COLOR_SOL = pg.Color(18, 18, 18)
COLOR_MUR = pg.Color(33, 33, 33)
COLOR_PROJECTILE = pg.Color(33, 33, 255)
COLOR_MONSTRE = pg.Color(255, 0, 0)


class VueCarte:
    """ Affichage de la carte """
    def __init__(self, carte, window):
        self.window = window
        self.carte = carte

        try:
            self.img_mage = pg.image.load("assets/mage.png")
        except pg.error:
            sys.exit(1)

        self.lig_scroll = 0
        self.col_scroll = 0

    def refresh(self, joueur):
        """ Affiche la carte sur la fenêtre """
        # Scrolling
        num_lines = self.window.height // TILE_SIZE
        num_cols = self.window.width // TILE_SIZE
        carte = self.carte
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= num_lines - 2 and self.lig_scroll <= carte.hauteur - num_lines:
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll -= 1
        elif joueur.col - self.col_scroll >= num_cols - 2 and self.col_scroll <= carte.largeur - num_cols:
            self.col_scroll += 1

        for lig in range(carte.hauteur):
            for col in range(carte.largeur):
                color = COLOR_SOL
                if carte.cases[lig][col] == SYMBOLE_MUR:
                    color = COLOR_MUR
                pg.draw.rect(
                    pg.display.get_surface(), color,
                    pg.Rect(lig * TILE_SIZE, col * TILE_SIZE, TILE_SIZE,
                            TILE_SIZE))

        # Affichage des projectiles
        for projectile in carte.projectiles:
            pg.draw.rect(
                pg.display.get_surface(), COLOR_PROJECTILE,
                pg.Rect(projectile.lig * TILE_SIZE, projectile.col * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE))

        # Affichage des monstres
        for entity in carte.entities:
            pg.draw.rect(
                pg.display.get_surface(), COLOR_MONSTRE,
                pg.Rect(entity.lig * TILE_SIZE, entity.col * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE))

        # Affichage du joueur
        pg.display.get_surface().blit(
            self.img_mage,
            pg.Rect(joueur.lig * TILE_SIZE, joueur.col * TILE_SIZE, TILE_SIZE,
                    TILE_SIZE))

    def center(self, joueur, window):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - window.height // 2
        self.col_scroll = joueur.col - window.width // 2
