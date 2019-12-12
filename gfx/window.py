# -*- coding: utf-8 -*-
""" La fenêtre principale affiche l'interface utilisateur
et gère les événements """

import sys
from time import sleep
from gettext import gettext

import pygame as pg
from pygame._sdl2 import messagebox

from entity import NORTH, SOUTH, WEST, EAST

## Durée (en s) d'un tour
FRAME_TIME = 1 / 15
## Code ASCII touche ECHAP
KEY_ESCAPE = 27

WINDOW_DEFAULT_WIDTH = 1000
WINDOW_DEFAULT_HEIGHT = 800


# pylint: disable=too-many-instance-attributes
class Window:
    """ Fenêtre SDL """
    def __init__(self):
        """" Initialisation des ressources """
        pg.init()
        pg.display.set_mode((WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT), 0,
                            32)

        # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # HP
        # curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Mana
        # curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Or
        # curses.init_pair(4, curses.COLOR_BLACK,
        #                  curses.COLOR_GREEN)  # Empoisonné
        # curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Maudit
        # curses.init_pair(6, curses.COLOR_MAGENTA,
        #                  curses.COLOR_GREEN)  # Poison & maudit

        self.should_close = False
        self.open_preferences = False

        self.width = WINDOW_DEFAULT_WIDTH
        self.height = WINDOW_DEFAULT_HEIGHT

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
        """ Ferme la fenêtre et libère les ressources """
        self.should_close = False
        pg.quit()

    def set_realtime(self, realtime):
        """ Mode temps réel """
        self.realtime = realtime

    def refresh(self):
        """ Gestion des événements """
        pg.display.flip()

        self.moving = 0
        self.shooting = False
        self.open_preferences = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.should_close = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.moving |= NORTH
                elif event.key == pg.K_DOWN:
                    self.moving |= SOUTH
                if event.key == pg.K_LEFT:
                    self.moving |= WEST
                elif event.key == pg.K_RIGHT:
                    self.moving |= EAST
                elif event.key == pg.K_a:
                    self.shooting = True
                elif event.key == pg.K_p:
                    self.open_preferences = True
                elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    self.should_close = True

        sleep(FRAME_TIME)

    def dialog(self, texte):
        """ Affiche une boîte de dialogue contenant :texte: """
        messagebox('Pyhack', texte)
