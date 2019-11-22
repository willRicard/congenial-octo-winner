# -*- coding: utf-8 -*-
""" La fenêtre principale affiche l'interface utilisateur
et gère les événements """

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
        """ Initialisation des ressources
        Le booléen :realtime: indique si on attend
        une action de l'utilisation pour rafraîchir """
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

        self.width = curses.COLS
        self.height = curses.LINES

        self.should_close = False
        self.resized = False
        self.open_preferences = False

        self.moving = 0
        self.shooting = False

    def close(self):
        """ Restaure le comportement par défaut du terminal """
        self.scr.keypad(False)
        curses.endwin()

    def set_realtime(self, realtime):
        """ Mode temps réel """
        self.scr.nodelay(realtime)
        self.realtime = realtime

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
            self.should_close = True
        elif key == curses.KEY_RESIZE:
            self.scr.clear()
            self.height, self.width = self.scr.getmaxyx()
            self.resized = True

        sleep(FRAME_TIME)

    def dialog(self, texte):
        """ Affiche une boîte de dialogue contenant :texte: """
        self.scr.nodelay(False)

        lignes = texte.split("\n")
        largeur = max(map(len, lignes)) + 3
        hauteur = len(lignes) + 2

        frame = curses.newwin(hauteur, largeur,
                              self.height // 2 - hauteur // 2,
                              self.width // 2 - largeur // 2)
        win = curses.newwin(hauteur - 2, largeur - 2,
                            self.height // 2 - hauteur // 2 + 1,
                            self.width // 2 - largeur // 2 + 1)

        try:
            frame.border()
            win.addstr(texte)
        except curses.error:
            sys.stderr.write(gettext("Votre terminal est trop petit !\n"))
            sys.exit(1)

        frame.noutrefresh()
        win.noutrefresh()

        self.refresh()

        self.scr.nodelay(self.realtime)
