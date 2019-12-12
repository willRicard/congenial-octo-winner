# -*- coding: utf-8 -*-
""" Affichage tête-haute """

import curses

from gettext import gettext

from gfx.window import COLOR_RED, COLOR_BLUE, COLOR_YELLOW

## @enum Mode d'affichage de l'ITH

## On affiche tout
DISPLAY_MODE_NORMAL = 0
## On n'affiche que les icônes la valeur
DISPLAY_MODE_NO_TEXT = 1
## On n'affiche que les icônes et le numérateur
DISPLAY_MODE_ICON = 2

## @enum Type de champ

## Un nombre
FIELD_TYPE_NUMBER = 0
## Un quotient ie. nombre/nombre
FIELD_TYPE_QUOTIENT = 1

## @enum Longueur du champ

## 3 chiffres max
NUMBER_FIELD_LENGTH = 3
## 2*3 chiffres max + 1 slash
QUOTIENT_FIELD_LENGTH = 2 * NUMBER_FIELD_LENGTH + 1

ITH_FIELDS = [("❤︎", "Vie", FIELD_TYPE_QUOTIENT, COLOR_RED),
              ("*", "Mana", FIELD_TYPE_QUOTIENT, COLOR_BLUE),
              ("$", "Or", FIELD_TYPE_NUMBER, COLOR_YELLOW)]


class ITH:
    """ Affichage tête haute """
    def __init__(self, window, display_mode):
        """ Précalcul des positions où afficher les champs """
        ## Fenêtre ncurses pour l'affichage
        self.win = curses.newwin(1, window.width, window.height - 1, 0)
        ## Mode d'affichage
        self.display_mode = display_mode
        ## Précalcul des positions des champs
        self.cols = [0] * len(ITH_FIELDS)

        # on n'affiche que les icônes si la fenêtre est trop petite
        try:
            self.draw_headers(
                icon_only=(self.display_mode == DISPLAY_MODE_ICON))
        except curses.error:
            self.draw_headers(icon_only=True)

    def draw_headers(self, icon_only=False):
        """ Affiche les en-têtes """
        col = 0
        for i, (icon, label, field_type, color) in enumerate(ITH_FIELDS):
            attr = curses.color_pair(color) | curses.A_BOLD
            if self.display_mode != DISPLAY_MODE_ICON:
                self.win.addstr(0, col, icon + " ", attr)
                col += 2  # espace entre icône et nom
            else:
                self.win.addstr(0, col, icon, attr)
                col += 1

            # on n'affiche pas le nom du champ
            # si la fenêtre n'est pas assez large.
            if not icon_only:
                self.win.addstr(0, col, gettext(label) + " ", attr)
                col += len(gettext(label)) + 1

            self.cols[i] = col

            # on laisse la place pour
            # remplir le champ
            if field_type == FIELD_TYPE_NUMBER or self.display_mode == DISPLAY_MODE_ICON:
                col += NUMBER_FIELD_LENGTH
            elif field_type == FIELD_TYPE_QUOTIENT:
                col += QUOTIENT_FIELD_LENGTH

    def refresh(self, joueur):
        """ Rafraîchit l'affichage de l'ITH """
        if self.display_mode != DISPLAY_MODE_ICON:
            champs = [
                '%3d/%3d' % (joueur.vie, joueur.max_vie),
                '%3d/%3d' % (joueur.mana, joueur.max_mana),
                str(joueur.gold)
            ]
        else:
            champs = [
                '%3d' % joueur.vie,
                '%3d' % joueur.mana,
                str(joueur.gold)
            ]

        for i, (_, _, _, color) in enumerate(ITH_FIELDS):
            self.win.addstr(0, self.cols[i], champs[i],
                            curses.color_pair(color) | curses.A_BOLD)

        self.win.noutrefresh()
