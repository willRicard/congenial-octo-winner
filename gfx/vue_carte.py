# -*- coding: utf-8 -*-
""" Affichage de la carte """

import sys

import pygame as pg

from carte import SYMBOLE_MUR, SYMBOLE_PROJECTILE
from joueur import POISON, CURSE
from gfx.window import WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT

TILE_SIZE = 16

LINES = WINDOW_DEFAULT_HEIGHT // TILE_SIZE
COLS = WINDOW_DEFAULT_WIDTH // TILE_SIZE

COLOR_SOL = pg.Color(18, 18, 18)
COLOR_MUR = pg.Color(33, 33, 33)


class VueCarte:
    """ Affichage de la carte """
    def __init__(self, carte):
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
        carte = self.carte
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= LINES - 2 and self.lig_scroll <= carte.hauteur - LINES:
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll -= 1
        elif joueur.col - self.col_scroll >= COLS - 2 and self.col_scroll <= carte.largeur - COLS:
            self.col_scroll += 1

        for lig in range(carte.hauteur):
            for col in range(carte.largeur):
                color = COLOR_SOL
                if carte.cases[lig][col] == SYMBOLE_MUR:
                    color = COLOR_MUR
                if carte.cases[lig][col] == SYMBOLE_PROJECTILE:
                    color == COLOR_PROJECTILE
                pg.draw.rect(
                    pg.display.get_surface(), color,
                    pg.Rect(lig * TILE_SIZE, col * TILE_SIZE, TILE_SIZE,
                            TILE_SIZE))

        # Affichage du joueur
        pg.display.get_surface().blit(
            self.img_mage,
            pg.Rect(joueur.lig * TILE_SIZE, joueur.col * TILE_SIZE, TILE_SIZE,
                    TILE_SIZE))

    def center(self, joueur):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - LINES // 2
        self.col_scroll = joueur.col - COLS // 2
