#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Bases de la Programmation Impérative : Projet Python """
import os
from random import seed, random
from gettext import gettext, bindtextdomain

from prefs import Preferences
from carte import Carte
from joueur import Joueur, NORTH, SOUTH, EAST, WEST, POISON, CURSE

from gfx.window import Window
from gfx.pref_dialog import PreferenceDialog
from gfx.vue_carte import VueCarte
from gfx.ith import ITH

INTRO_TEXTE = "Bienvenue, aventurier !\n\
Vous avez parcouru un long chemin pour arriver ici en quête de gloire.\n\
Vous entrez maintenant dans les donjons d'Eneladim.\n\n\
Pourrez vous faire face aux fléaux de cet endroit?\n\n\
Appuyez sur 'p' pour éditer vos préférences.\n\n\
Appuyez sur Échap. pour quitter.\n\
Appuyez sur Entrée pour continuer."

ERREUR_TEXTE = "Impossible de lire/écrire vos préférences depuis {}\
Vérifiez vos permissions !\n{}"

PROBA_ALTERATION = 0.05


def charger_preferences(path):
    """ Chargement / définition des préférences """
    prefs = Preferences()

    try:
        prefs.restore(path)
    except FileNotFoundError:
        update_preferences(prefs, path)

    return prefs


def update_preferences(prefs, path):
    """ Affiche le formulaire de configuration puis enregistre les options. """
    PreferenceDialog(prefs).show()
    prefs.save(path)


def main():
    """ Point d'entrée du programme """
    seed(0)
    bindtextdomain("messages", ".")

    window = Window()

    pref_file = os.getenv("HOME") + os.sep + ".pyhack"
    try:
        prefs = charger_preferences(pref_file)
    except OSError as err:
        window.dialog(gettext(ERREUR_TEXTE).format(path, err.strerror))

    window.set_realtime(prefs.realtime)

    # Message d'accueil
    window.dialog(gettext(INTRO_TEXTE))

    carte = Carte(64, 128)
    carte.generer_salles()

    view = VueCarte(carte, window)

    depart = carte.salles[0]
    col, lig = depart.centre()
    joueur = Joueur(lig, col)
    ith = ITH(window, prefs.icon_only)

    view.center(joueur, window)

    while not window.should_close:
        # On inflige une altération d'état aléatoire au joueur
        # avec une certaine probabilité
        if random() < PROBA_ALTERATION:
            if random() < 0.5 and not joueur.aliment & POISON:
                joueur.aliment |= POISON
                window.dialog(gettext('Les miasmes du donjon vous ont empoisonné !'))
            elif not joueur.aliment & CURSE:
                joueur.aliment |= CURSE
                window.dialog(gettext('Le donjon absorbe votre énergie magique !'))

        if joueur.vie == 0:
            window.dialog('Game over !')
            break

        joueur.update()
        carte.update(joueur)

        view.refresh(joueur, window)
        ith.refresh(joueur)
        window.refresh()

        if window.resized:
            view = VueCarte(carte, window)
            view.refresh(joueur, window)
            ith = ITH(window, prefs.icon_only)
            ith.refresh(joueur)

        if window.open_preferences:
            try:
                update_preferences(prefs, pref_file)
            except OSError as err:
                window.dialog(gettext(ERREUR_TEXTE).format(path, err.strerror))
            window.set_realtime(prefs.realtime)

        if window.moving & NORTH and carte.case_libre(joueur.lig - 1,
                                                      joueur.col):
            joueur.lig -= 1
            joueur.facing = NORTH
        elif window.moving & SOUTH and carte.case_libre(
                joueur.lig + 1, joueur.col):
            joueur.lig += 1
            joueur.facing = SOUTH
        if window.moving & WEST and carte.case_libre(joueur.lig,
                                                     joueur.col - 1):
            joueur.col -= 1
            joueur.facing = WEST
        elif window.moving & EAST and carte.case_libre(joueur.lig,
                                                       joueur.col + 1):
            joueur.col += 1
            joueur.facing = EAST

        if window.shooting:
            joueur.shoot(carte)

    window.close()


if __name__ == "__main__":
    main()
