# -*- coding: utf-8 -*-
""" Affichage de la carte """

import curses
from carte import SYMBOLE_MUR, SYMBOLE_PROJECTILE
from joueur import POISON, CURSE


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
                    attr = curses.color_pair(2)
                self.pad.addstr(lig, col, carte.cases[lig][col], attr)

        # Affichage du joueur
        attr = curses.A_REVERSE
        if joueur.aliment == POISON:
            attr = curses.color_pair(4)
        elif joueur.aliment == CURSE:
            attr = curses.color_pair(5)
        elif joueur.aliment == POISON | CURSE:
            attr = curses.color_pair(6)

        self.pad.addstr(joueur.lig, joueur.col, '@', attr)

        # On laisse la derinière ligne pour l'ITH
        try:
            self.pad.refresh(self.lig_scroll, self.col_scroll, 0, 0,
                             window.height - 2, window.width - 1)
        except curses.error:
            pass

    def center(self, joueur, window):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - window.height // 2
        self.col_scroll = joueur.col - window.width // 2
