# -*- coding: utf-8 -*-
""" Formulaire de configuration """
import sys
import curses
from gettext import gettext
from time import sleep

from gfx.window import FRAME_TIME, KEY_ESCAPE

PREF_DIALOG_START_LIG = 2  # Ligne où démarrer l'affichage des options. Doit être positive.
PREF_DIALOG_START_COL = 3  # Colonne où démarrer l'affichage des options. Doit être positive.
PREF_DIALOG_LIG_STEP = 2  # Espace entre deux options

PREF_DIALOG_VERTICAL_PADDING = 7  # Marge verticale. Crash si < 7
PREF_DIALOG_HORIZONTAL_PADDING = 16  # Marge horizontale. Crash si < 16


class PreferenceDialog:
    """ Formulaire de configuration """
    def __init__(self, prefs=None):
        self.prefs = prefs

        titres = [gettext("Mode de jeu"), gettext("Difficulté")]

        self.champs = [[gettext("Tour par tour"),
                        gettext("Temps réel")],
                       [
                           gettext("Facile"),
                           gettext("Normale"),
                           gettext("Difficile")
                       ]]
        self.champ_sel = 0
        self.choix = [0] * len(self.champs)
        self.choix[0] = int(prefs.realtime)
        self.choix[1] = prefs.difficulty
        self.cols = []  # précalcul des positions pour chaque label

        hauteur = 2 * len(self.champs) + PREF_DIALOG_VERTICAL_PADDING
        largeur = max([
            len(titres[i]) + len(" ".join(champ))
            for i, champ in enumerate(self.champs)
        ]) + PREF_DIALOG_HORIZONTAL_PADDING

        try:
            self.win = curses.newwin(hauteur, largeur,
                                     curses.LINES // 2 - hauteur // 2,
                                     curses.COLS // 2 - largeur // 2)
        except curses.error:
            sys.stderr.write(gettext("Votre terminal est trop petit !\n"))
            sys.exit(1)

        self.win.border()
        self.win.keypad(True)
        titre = gettext("Configuration")
        self.win.addstr(0, largeur // 2 - len(titre) // 2, titre)

        # On remplit la fenetre avec les valeurs
        lig, col = PREF_DIALOG_START_LIG, PREF_DIALOG_START_COL
        for i, champ in enumerate(self.champs):
            cols_champ = []
            titre = titres[i]
            col = PREF_DIALOG_START_COL
            self.win.addstr(lig, col, titre, curses.A_BOLD)
            col += len(titre) + 1  # espace
            for j, option in enumerate(champ):
                cols_champ.append(col)
                if j == self.choix[i]:
                    self.win.addstr(lig, col, option, curses.A_REVERSE)
                else:
                    self.win.addstr(lig, col, option)
                col += len(option) + 1  # espace
            lig += PREF_DIALOG_LIG_STEP
            self.cols.append(cols_champ)

        self.win.addstr(lig, 1, "-" * (largeur - 2))
        lig += 1
        self.win.addstr(
            lig, 1,
            gettext("Choisissez vos options avec les touches fléchées."))
        lig += 1
        self.win.addstr(lig, 1, gettext("Validez avec Entrée."))
        lig += 1
        self.win.addstr(lig, 1, gettext("Quittez avec Échap."))

        lig = PREF_DIALOG_START_LIG + PREF_DIALOG_LIG_STEP * self.champ_sel
        self.win.addch(lig, 1, ">")

    def affiche_choix(self, attr):
        """Affiche le label du :choix: pour le champ selectionné avec
        l'attribut curses de mise en forme :attr: """
        self.win.addstr(
            PREF_DIALOG_START_LIG + PREF_DIALOG_LIG_STEP * self.champ_sel,
            self.cols[self.champ_sel][self.choix[self.champ_sel]],
            self.champs[self.champ_sel][self.choix[self.champ_sel]], attr)

    def show(self):
        """ Affiche le formulaire et modifie les préférences choisies par l'utilisateur. """
        lig = PREF_DIALOG_START_LIG + PREF_DIALOG_LIG_STEP * self.champ_sel
        while True:
            key = self.win.getch()
            if key == curses.KEY_UP and self.champ_sel > 0:
                self.win.addch(lig, 1, " ")
                self.champ_sel -= 1
                lig -= PREF_DIALOG_LIG_STEP
                self.win.addch(lig, 1, ">")
            elif key == curses.KEY_DOWN and self.champ_sel < len(
                    self.champs) - 1:
                self.win.addch(lig, 1, " ")
                self.champ_sel += 1
                lig += PREF_DIALOG_LIG_STEP
                self.win.addch(lig, 1, ">")
            elif key == curses.KEY_LEFT and self.choix[self.champ_sel] > 0:
                self.affiche_choix(curses.A_NORMAL)
                self.choix[self.champ_sel] -= 1
                self.affiche_choix(curses.A_REVERSE)
            elif key == curses.KEY_RIGHT and self.choix[self.champ_sel] < len(
                    self.champs[self.champ_sel]) - 1:
                self.affiche_choix(curses.A_NORMAL)
                self.choix[self.champ_sel] += 1
                self.affiche_choix(curses.A_REVERSE)
            elif key in (curses.KEY_ENTER, KEY_ESCAPE):
                break

            self.win.refresh()
            sleep(FRAME_TIME)

        self.prefs.realtime = bool(self.choix[0])
        self.prefs.difficulty = self.choix[1]

        self.win.clear()
        self.win.refresh()