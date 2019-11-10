# -*- coding: utf-8 -*-
""" La fenêtre principale affiche l'interface utilisateur et gère les événements """

import sys
import curses
from time import sleep
from gettext import gettext

from joueur import NORTH, SOUTH, WEST, EAST

FRAME_TIME = 1 / 15
KEY_ESCAPE = 27


class Window:
    """ Fenêtre dans le terminal """
    def __init__(self):
        """Initialisation des ressources
        Le booléen :realtime: indique si on attend une action de l'utilisation pour rafraîchir.
        """
        self.scr = curses.initscr()
        self.scr.keypad(True)
        curses.curs_set(0)
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

        self.scr.clear()
        self.scr.refresh()

        self.moving = 0
        self.shooting = False
        self.open_preferences = False

    def close(self):
        """ Restaure le comportement par défaut du terminal """
        self.scr.keypad(False)
        curses.endwin()

    def set_realtime(self, realtime):
        """ Mode temps réel """
        self.scr.nodelay(realtime)

    def refresh(self):
        """ Gestion des événements """
        self.scr.refresh()

        key = self.scr.getch()

        self.moving = 0
        self.shooting = False
        self.open_preferences = False
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
        elif key == ord('p'):
            self.open_preferences = True
        elif key == ord('q') or key == KEY_ESCAPE:
            sys.exit(0)

        sleep(FRAME_TIME)


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
        sys.stderr.write(gettext("Votre terminal est trop petit !\n"))
        sys.exit(1)

    frame.refresh()

    key = win.getstr()
    if key == chr(27):  # Echap
        sys.exit(0)
    frame.clear()
    frame.refresh()
