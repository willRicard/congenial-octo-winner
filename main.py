#!/usr/bin/env python
""" Project Python Semestre 1 """
from random import seed, random, choice
from gettext import gettext, bindtextdomain
import curses
import sys

from carte import Carte
from joueur import Joueur

from config import NORTH, SOUTH, EAST, WEST, POISON, CURSE
from util import dialog

INTRO_TEXTE = gettext("Bienvenue, aventurier !\n\
Vous avez parcouru un long chemin pour arriver ici en quête de gloire.\n\
Vous entrez maintenant dans les donjons d'Eneladim.\n\n\
Pourrez vous faire face aux fléaux de cet endroit?\n\n\
Appuyez sur Échap. pour quitter.\n\
Appuyez sur Entrée pour continuer.")


def main(stdscr):
    """ Point d'entrée du programme """
    bindtextdomain("messages", ".")

    # Message d'accueil
    dialog(INTRO_TEXTE)

    carte = Carte(64, 128)
    #carte = Carte(100, 100)
    #carte.generer_salles()
    carte.generer_salles_partitionnement()

    # Départ dans une salle aléatoire
    depart = choice(carte.salles)
    col, lig = depart.centre()
    joueur = Joueur(lig, col)

    # On centre l'écran sur le joueur
    carte.lig_scroll = joueur.lig - curses.LINES // 2
    carte.col_scroll = joueur.col - curses.COLS // 2

    while True:
        # On inflige une altération d'état aléatoire au joueur
        # avec une certaine probabilité
        if random() < 0.05:
            if random() < 0.5 and not joueur.aliment & POISON:
                joueur.aliment |= POISON
                dialog(gettext('Les miasmes du donjon vous ont empoisonné !'))
            elif not joueur.aliment & CURSE:
                joueur.aliment |= CURSE
                dialog(gettext('Le donjon absorbe votre énergie magique !'))

        if joueur.vie == 0:
            dialog('Game over !')
            break

        carte.affiche()
        joueur.update()
        carte.update(joueur)
        joueur.affiche_ith(stdscr)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and carte.case_libre(joueur.lig - 1,
                                                     joueur.col):
            joueur.lig -= 1
            joueur.facing = NORTH
        elif key == curses.KEY_DOWN and carte.case_libre(
                joueur.lig + 1, joueur.col):
            joueur.lig += 1
            joueur.facing = SOUTH
        elif key == curses.KEY_LEFT and carte.case_libre(
                joueur.lig, joueur.col - 1):
            joueur.col -= 1
            joueur.facing = EAST
        elif key == curses.KEY_RIGHT and carte.case_libre(
                joueur.lig, joueur.col + 1):
            joueur.col += 1
            joueur.facing = WEST
        elif key == ord('a'):
            joueur.shoot(carte)
        elif key == ord('q') or key == 27:  # Escape
            break


if __name__ == "__main__":
    # seed(0)
    curses.wrapper(main)
