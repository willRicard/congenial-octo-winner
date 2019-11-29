# -*- coding: utf-8 -*-
""" Affichage de la carte """
import curses
from carte import SYMBOLE_JOUEUR, SYMBOLE_SOL, SYMBOLE_MUR, SYMBOLE_MONSTRE, SYMBOLE_PROJECTILE
from joueur import ALIMENT_POISON, ALIMENT_CURSE

from monstre.rat import Rat
from monstre.monstre import Monstre

from gfx.window import COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_MAGENTA, COLOR_GREEN_MAGENTA


class VueCarte:
    """ Affichage de la carte """

    def __init__(self, carte, window):
        self.carte = carte

        self.pad = curses.newpad(carte.hauteur + 1, carte.largeur + 1)

        self.lig_scroll = 0
        self.col_scroll = 0

    def refresh(self, joueur, window):
        """ Affiche la carte sur un écran ncurses :scr: """
        # Scrolling
        carte = self.carte
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= window.height - 2 and self.lig_scroll <= carte.hauteur - window.height:
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll -= 1
        elif joueur.col - self.col_scroll >= window.width - 2 and self.col_scroll <= carte.largeur - window.width:
            self.col_scroll += 1

        for lig in range(carte.hauteur):
            for col in range(carte.largeur):
                attr = curses.A_NORMAL
                if carte.cases[lig][col] == SYMBOLE_MUR:
                    attr = curses.A_REVERSE
                if carte.cases[lig][col] == SYMBOLE_PROJECTILE:
                    attr = curses.color_pair(COLOR_BLUE)
                self.pad.addstr(lig, col, carte.cases[lig][col], attr)

        # Affichage des projectiles
        for projectile in carte.projectiles:
            self.pad.addstr(projectile.lig, projectile.col, SYMBOLE_PROJECTILE,
                            curses.color_pair(COLOR_BLUE))

        # Affichage des monstres
        for entity in carte.entities:
            symbole = ""
            if isinstance(entity, Rat):
                symbole = "r"
            elif isinstance(entity, Monstre):
                symbole = "X"

            self.pad.addstr(entity.lig, entity.col, symbole,
                            curses.color_pair(COLOR_RED))

        # Affichage du joueur
        attr = curses.A_REVERSE
        if joueur.aliment == ALIMENT_POISON:
            attr = curses.color_pair(COLOR_GREEN)
        elif joueur.aliment == ALIMENT_CURSE:
            attr = curses.color_pair(COLOR_MAGENTA)
        elif joueur.aliment == ALIMENT_POISON | ALIMENT_CURSE:
            attr = curses.color_pair(COLOR_GREEN_MAGENTA)

        self.pad.addstr(joueur.lig, joueur.col, SYMBOLE_JOUEUR, attr)

        # On laisse la derinière ligne pour l'ITH
        try:
            self.pad.refresh(self.lig_scroll, self.col_scroll, 0, 0,
                             window.height - 2, window.width - 1)
        except Exception:
            pass

    def center(self, joueur, window):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - window.height // 2
        self.col_scroll = joueur.col - window.width // 2
