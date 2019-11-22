# -*- coding: utf-8 -*-
""" Affichage tête-haute """

import curses

from gettext import gettext

# @enum Couleur de fond pour un champ
COLOR_RED = 1
COLOR_BLUE = 2
COLOR_YELLOW = 3

# @enum Type de champ
FIELD_TYPE_NUMBER = 0  # un nombre
FIELD_TYPE_QUOTIENT = 1  # un quotient: nombre/nombre

NUMBER_FIELD_LENGTH = 3  # 3 chiffres max
QUOTIENT_FIELD_LENGTH = 7  # 2*3 chiffres max + 1 slash

ITH_FIELDS = [("❤︎", "Vie", FIELD_TYPE_QUOTIENT,
               COLOR_RED), ("*", "Mana", FIELD_TYPE_QUOTIENT, COLOR_BLUE),
              ("$", "Or", FIELD_TYPE_NUMBER, COLOR_YELLOW)]


class ITH:
    """ Affichage tête haute """

    def __init__(self, window, icon_only):
        """ Précalcul des positions où afficher les champs """
        self.win = curses.newwin(1, window.width, window.height - 1, 0)
        self.icon_only = icon_only
        self.cols = []

        # on n'affiche que les icônes si la fenêtre est trop petite
        try:
            self.draw_headers(self.icon_only)
        except curses.error:
            self.draw_headers(icon_only=True)

    def draw_headers(self, icon_only=False):
        """ Affiche les en-têtes """
        col = 0
        for icon, label, field_type, color in ITH_FIELDS:
            attr = curses.color_pair(color) | curses.A_BOLD
            self.win.addstr(0, col, icon + " ", attr)
            col += 2  # espace entre icône et nom

            # on n'affiche pas le nom du champ
            # si la fenêtre n'est pas assez large.
            if not icon_only:
                self.win.addstr(0, col, gettext(label) + " ", attr)
                col += len(gettext(label)) + 1

            self.cols.append(col)

            # on laisse la place pour
            # remplir le champ
            if field_type == FIELD_TYPE_QUOTIENT:
                col += QUOTIENT_FIELD_LENGTH
            elif field_type == FIELD_TYPE_NUMBER:
                col += NUMBER_FIELD_LENGTH

    def refresh(self, joueur):
        """ Rafraîchit l'affichage de l'ITH """
        champs = [
            '%3d/%3d' % (joueur.vie, joueur.max_vie),
            '%3d/%3d' % (joueur.mana, joueur.max_mana),
            str(joueur.gold)
        ]

        for i, (_, _, _, color) in enumerate(ITH_FIELDS):
            self.win.addstr(0, self.cols[i], champs[i],
                            curses.color_pair(color) | curses.A_BOLD)

        self.win.noutrefresh()
