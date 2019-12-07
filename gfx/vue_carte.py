# -*- coding: utf-8 -*-
""" Affichage de la carte """
import sys
import pygame as pg

from joueur import ALIMENT_POISON, ALIMENT_CURSE

from monstre.rat import Rat
from monstre.goblin import Goblin

TILE_SIZE = 16

COLOR_SOL = pg.Color(18, 18, 18)
COLOR_MUR = pg.Color(33, 33, 33)
COLOR_PROJECTILE = pg.Color(33, 33, 255)
COLOR_MONSTRE = pg.Color(255, 0, 0)


class VueCarte:
    """ Affichage de la carte """
    def __init__(self, carte):
        """ Constructeur """
        ## Référence vers la carte
        self.carte = carte

        self.surface = pg.Surface(pg.display.get_window_size())

        try:
            self.img_mage = pg.image.load("assets/mage.png")
        except pg.error:
            sys.exit(1)

        ## Ordonnée du coin supérieur gauche de la vue affichée
        self.lig_scroll = 0
        ## Abscisse du coin supérieur gauche de la vue affichée
        self.col_scroll = 0

    def refresh(self, joueur, window):
        """ Affiche la carte sur la fenêtre """
        # Scrolling
        num_lines = window.height // TILE_SIZE
        num_cols = window.width // TILE_SIZE
        carte = self.carte
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= num_lines - 2 and self.lig_scroll <= carte.hauteur - num_lines:
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll += 1
        elif joueur.col - self.col_scroll >= num_cols - 2 and self.col_scroll <= carte.largeur - num_cols:
            self.col_scroll -= 1

        # Affichage de la carte
        for lig in range(carte.hauteur):
            for col in range(carte.largeur):
                color = COLOR_MUR
                if carte.cases[lig] & 1 << col:
                    color = COLOR_SOL
                pg.draw.rect(
                    self.surface, color,
                    pg.Rect(col * TILE_SIZE, lig * TILE_SIZE, TILE_SIZE,
                            TILE_SIZE))

        # Affichage des projectiles
        for projectile in carte.projectiles:
            pg.draw.rect(
                self.surface, COLOR_PROJECTILE,
                pg.Rect(projectile.col * TILE_SIZE, projectile.lig * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE))

        # Affichage des monstres
        for entity in carte.entities:
            pg.draw.rect(
                self.surface, COLOR_MONSTRE,
                pg.Rect(entity.col * TILE_SIZE, entity.lig * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE))

        # Affichage du joueur
        self.surface.blit(
            self.img_mage,
            pg.Rect(joueur.col * TILE_SIZE, joueur.lig * TILE_SIZE, TILE_SIZE,
                    TILE_SIZE))

        pg.display.get_surface().blit(
            self.surface,
            pg.Rect(self.col_scroll * TILE_SIZE, self.lig_scroll * TILE_SIZE,
                    num_cols * TILE_SIZE, num_lines * TILE_SIZE))

    def center(self, joueur, window):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - window.height // 2
        self.col_scroll = joueur.col - window.width // 2
