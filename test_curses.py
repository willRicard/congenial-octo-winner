#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses


def generer_carte():
    carte = []
    for lig in range(32):
        ligne = []
        for col in range(32):
            if lig == 3 and col == 2:
                ligne.append('@')
            else:
                ligne.append('.')
        carte.append(ligne)
    return carte


def affiche_carte(scr, carte):
    for lig in range(min(32, curses.LINES - 1)):
        for col in range(min(32, curses.COLS - 1)):
            ch = carte[lig][col]
            attr = curses.A_NORMAL
            if ch == '@':
                attr = curses.A_REVERSE
            scr.addstr(lig, col, ch, attr)


def main(stdscr):
    carte = generer_carte()
    lig_joueur, col_joueur = 3, 2

    stdscr.clear()

    while True:
        affiche_carte(stdscr, carte)
        key = stdscr.getkey()
        if key == "KEY_UP":
            carte[lig_joueur][col_joueur] = '.'
            lig_joueur -= 1
            carte[lig_joueur][col_joueur] = '@'
        elif key == "KEY_DOWN":
            carte[lig_joueur][col_joueur] = '.'
            lig_joueur += 1
            carte[lig_joueur][col_joueur] = '@'
        elif key == "KEY_LEFT":
            carte[lig_joueur][col_joueur] = '.'
            col_joueur -= 1
            carte[lig_joueur][col_joueur] = '@'
        elif key == "KEY_LEFT":
            carte[lig_joueur][col_joueur] = '.'
            lig_joueur -= 1
            carte[lig_joueur][col_joueur] = '@'
        elif key == "KEY_RIGHT":
            carte[lig_joueur][col_joueur] = '.'
            col_joueur += 1
            carte[lig_joueur][col_joueur] = '@'
        elif key == chr(27):  # Escape
            break

    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    curses.wrapper(main)
