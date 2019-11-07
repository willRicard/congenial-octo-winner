# -*- coding: utf-8 -*-
""" Affichage tête-haute """

import curses

from gettext import gettext

ITH_FIELDS = ["❤︎ Vie", "* Mana", "$ Or"]
ITH_NUMBER_FIELD_LENGTH = 7  # 2*3 chiffres + 1 slash


class ITH:
    def __init__(self):
        """ Précalcul des positions où afficher les champs """
        self.win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        self.ith_cols = []

        col = 0
        for i, field in enumerate(ITH_FIELDS):
            col += len(gettext(field))
            self.win.addstr(0, col, gettext(field), curses.color_pair(i + 1) | curses.A_BOLD)
            self.ith_cols.append(col)
            col += ITH_NUMBER_FIELD_LENGTH

        self.win.addstr(
            0, self.ith_cols[-1],
            gettext(
                ' < ^ v > déplacement | a attaque | b parade | p ramasser'))

    def refresh(self, joueur):
        for i, ch in enumerate([
                str(joueur.vie) + '/' + str(joueur.max_vie),
                str(joueur.mana) + '/' + str(joueur.max_mana),
                str(joueur.gold)
        ]):
            self.win.addstr(0, self.ith_cols[i], ch, curses.color_pair(i + 1) | curses.A_BOLD)


        self.win.refresh()
