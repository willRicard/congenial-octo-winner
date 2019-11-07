# -*- coding: utf-8 -*-

import curses
from gettext import gettext

from joueur import NORTH, SOUTH, WEST, EAST


class Window:
    """ Fenêtre dans le terminal """
    def __init__(self):
        """ Initialisation des ressources """
        self.scr = curses.initscr()
        self.scr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # HP
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Mana
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Or
        curses.init_pair(4, curses.COLOR_BLACK,
                         curses.COLOR_GREEN)  # Empoisonné
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Maudit
        curses.init_pair(6, curses.COLOR_MAGENTA,
                         curses.COLOR_GREEN)  # Poison & maudit

        self.moving = 0
        self.shooting = False

    def close():
        """ Restaure le comportement par défaut du terminal """
        curses.endwin()

    def refresh(self):
        """ Gestion des événements """
        key = self.scr.getch()

        self.moving = 0
        self.shooting = False
        if key == curses.KEY_UP:
            self.moving |= NORTH
        elif key == curses.KEY_DOWN:
            self.moving |= SOUTH
        if key == curses.KEY_LEFT:
            self.moving |= WEST
        elif key == curses.KEY_RIGHT:
            self.moving |= EAST
        elif key == ord('a'):
            self.shooting = True
        elif key == ord('q') or key == 27:  # Escape
            exit()


def dialog(texte):
    """ Affiche une boîte de dialogue contenant :texte: """
    lignes = texte.split("\n")
    largeur = max(map(len, lignes)) + 3
    hauteur = len(lignes) + 2

    frame = curses.newwin(hauteur, largeur, curses.LINES // 2 - hauteur // 2,
                          curses.COLS // 2 - largeur // 2)
    win = curses.newwin(hauteur - 2, largeur - 2,
                        curses.LINES // 2 - hauteur // 2 + 1,
                        curses.COLS // 2 - largeur // 2 + 1)

    try:
        frame.border()
        win.addstr(texte)
    except curses.error:
        # Votre terminal est trop petit !
        pass
    frame.refresh()

    key = win.getstr()
    if key == chr(27):  # Echap
        sys.exit(0)
    frame.clear()
    frame.refresh()
