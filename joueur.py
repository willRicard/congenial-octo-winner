#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Joueur et Interface Tête Haute """

import curses
from gettext import gettext

from config import NORTH, SOUTH, EAST, WEST, BASE_VIE, BASE_MANA, BASE_GOLD, POISON, CURSE


class Joueur():
    """ Joueur représenté par un @ """
    def __init__(self, lig, col):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # HP
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Mana
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Or
        curses.init_pair(4, curses.COLOR_BLACK,
                         curses.COLOR_GREEN)  # Empoisonne
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Maudit
        curses.init_pair(6, curses.COLOR_MAGENTA,
                         curses.COLOR_GREEN)  # Poison & maudit

        self.lig = lig
        self.col = col
        self.facing = NORTH

        self.vie = self.max_vie = BASE_VIE

        self.mana = self.max_mana = BASE_MANA

        self.level = 1
        self.exp = 0
        self.gold = BASE_GOLD
        self.aliment = 0

    def update(self):
        """ Met a jour l'etat du joueur suivant ses altérations d'état. """
        from random import random
        if self.aliment & POISON and random() < 0.2:
            self.vie -= 1
        if self.aliment & CURSE and self.mana > 0 and random() < 0.2:
            self.mana -= 1

    def affiche(self, scr):
        """ Affiche le joueur """
        attr = curses.A_REVERSE
        if self.aliment == POISON:
            attr = curses.color_pair(4)
        elif self.aliment == CURSE:
            attr = curses.color_pair(5)
        elif self.aliment == POISON | CURSE:
            attr = curses.color_pair(6)

        scr.addstr(self.lig, self.col, '@', attr)

    def affiche_ith(self, scr):
        """ Affiche l'interface tête haute pour le joueur """
        scr.addstr(curses.LINES - 1, 0, ' ' * (curses.COLS - 1))
        scr.refresh()
        col = 0

        ith = [
            gettext('❤︎ Vie {}/{} ').format(self.vie, self.max_vie),
            gettext(' ❇︎ Mana {}/{} ').format(self.mana, self.max_mana),
            gettext(' $ Or {} ').format(self.gold)
        ]

        for i, string in enumerate(ith):
            scr.addstr(curses.LINES - 1, col, string,
                       curses.color_pair(i + 1) | curses.A_BOLD)
            col += len(string)

        try:
            scr.addstr(
                curses.LINES - 1, col,
                gettext(
                    ' < ^ v > déplacement | a attaque | b parade | p ramasser'))
        except:
            # Terminal trop petit!
            pass

    def level_up(self):
        """ Augmente les attributs du joueur """
        self.max_vie += self.level
        self.vie = self.vie

        self.max_mana += self.level
        self.mana = self.max_mana

    def shoot(self, carte):
        """ Tire un projectile devant le joueur. """
        lig, col = self.lig, self.col
        if self.facing == NORTH:
            lig -= 1
        elif self.facing == SOUTH:
            lig += 1
        elif self.facing == WEST:
            col += 1
        elif self.facing == EAST:
            col -= 1

        if self.mana > 0:
            self.mana -= 1
            carte.projectiles.append([lig, col, self.facing])
            carte.cases[lig][col] = '❇︎'
