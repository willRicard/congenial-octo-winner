# -*- coding: utf-8 -*-
""" La fenêtre principale affiche l'interface utilisateur
et gère les événements """

import sys
import curses
from time import time, sleep
from gettext import gettext

from entity import NORTH, SOUTH, WEST, EAST

## @enum Couleur d'affichage
COLOR_RED = 1
COLOR_BLUE = 2
COLOR_YELLOW = 3
COLOR_GREEN = 4
COLOR_MAGENTA = 5
COLOR_GREEN_MAGENTA = 6

FRAME_TIME = 1 / 15  # Durée (en s) d'un tour
KEY_ESCAPE = 27  # Code ASCII touche ECHAP


# pylint: disable=too-many-instance-attributes
class Window:
    """ Fenêtre dans le terminal """
    def __init__(self):
        """ Initialisation des ressources
        Le booléen :realtime: indique si on attend
        une action de l'utilisation pour rafraîchir """
        ## Écran ncurses
        self.scr = curses.initscr()
        self.scr.keypad(True)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

        curses.init_pair(COLOR_RED, curses.COLOR_WHITE, curses.COLOR_RED)  # HP
        curses.init_pair(COLOR_BLUE, curses.COLOR_WHITE,
                         curses.COLOR_BLUE)  # Mana
        curses.init_pair(COLOR_YELLOW, curses.COLOR_BLACK,
                         curses.COLOR_YELLOW)  # Or
        curses.init_pair(COLOR_GREEN, curses.COLOR_BLACK,
                         curses.COLOR_GREEN)  # Empoisonné
        curses.init_pair(COLOR_MAGENTA, curses.COLOR_BLACK,
                         curses.COLOR_MAGENTA)  # Maudit
        curses.init_pair(COLOR_GREEN_MAGENTA, curses.COLOR_MAGENTA,
                         curses.COLOR_GREEN)  # Poison & maudit

        self.scr.clear()
        self.scr.refresh()

        height, width = self.scr.getmaxyx()
        ## Nombre de colonnes
        self.width = width
        ## Nombre de lignes
        self.height = height

        ## Indique si le jeu attend une
        # action du joueur avant de se mettre à jour
        self.realtime = False
        ## Timestamp of the last frame
        self.last_frame = 0

        ## Indique si la fenêtre doit se fermer
        self.should_close = False
        ## Indique si la fenêtre vient d'être redimensionnée
        self.resized = False
        ## Indique si on doit afficher l'éditeur de préférences
        self.open_preferences = False

        ## Direction de déplacement
        self.moving = 0
        ## Indique si le joueur doit tirer
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

        self.moving = 0
        self.shooting = False
        self.open_preferences = False

        key = self.scr.getch()
        while key != -1:
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

            if self.realtime:
                key = self.scr.getch()
            else:
                key = -1

        if self.realtime:
            now = time()
            if now - self.last_frame < FRAME_TIME:
                sleep(FRAME_TIME - now + self.last_frame)
            self.last_frame = time()

    def dialog(self, texte):
        """ Affiche une boîte de dialogue contenant :texte: """
        realtime = self.realtime
        self.set_realtime(False)

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

        self.set_realtime(realtime)
