#!/usr/bin/env python
""" Utilitaires d'affichage """

import curses

def dialog(texte):
    """ Affiche l'écran titre """
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
        raise Exception(gettext('Votre terminal est trop petit !'))
    frame.refresh()

    key = win.getstr()
    if key == chr(27):  # Echap
        sys.exit(0)
    frame.clear()
    frame.refresh()

class DummyScreen:
    """ Écran ncurses émulé: n'affiche rien """
    def __init__(self):
        """ Constructeur vide """
        pass

    def clear(self):
        """ Stub """
        pass

    def addstr(self, *args):
        """ Stub """
        pass

    def refresh(self):
        """ Stub """
        pass

    def getkey(self):
        """ Stub """
        return chr(27)
