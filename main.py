#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Bases de la Programmation Impérative : Projet Python """
import os
from gettext import gettext, bindtextdomain

from prefs import Preferences
from carte import Carte
from joueur import Joueur

from gfx.window import Window
from gfx.pref_dialog import PreferenceDialog
from gfx.vue_carte import VueCarte
from gfx.ith import ITH

## Texte affiché à l'ouverture du jeu
INTRO_TEXTE = "Bienvenue, aventurier !\n\
Vous avez parcouru un long chemin pour arriver ici en quête de gloire.\n\
Vous entrez maintenant dans les donjons d'Eneladim.\n\n\
Pourrez vous faire face aux fléaux de cet endroit?\n\n\
Appuyez sur 'p' pour éditer vos préférences.\n\n\
Appuyez sur Échap. pour quitter.\n\
Appuyez sur Entrée pour continuer."

## Texte affiché en cas d'erreur au niveau
# du système de fichiers
ERREUR_TEXTE = "Impossible de lire/écrire vos préférences depuis {}\
Vérifiez vos permissions !\n{}"


def charger_preferences(path, window):
    """ Chargement / définition des préférences """
    prefs = Preferences()

    try:
        prefs.restore(path)
    except FileNotFoundError:
        PreferenceDialog(prefs, window).show()
        prefs.save(path)

    return prefs


def update_preferences(prefs, path, window):
    """ Affiche le formulaire de configuration puis enregistre les options. """
    try:
        PreferenceDialog(prefs, window).show()
        prefs.save(path)
    except OSError as err:
        window.dialog(gettext(ERREUR_TEXTE).format(path, err.strerror))


def main():
    """ Point d'entrée du programme """
    # chargement des messages traduits
    bindtextdomain("messages", ".")

    window = Window()

    pref_file = os.path.join(os.getenv("HOME"), ".pyhack-ricardgu")
    try:
        prefs = charger_preferences(pref_file, window)
    except OSError as err:
        window.dialog(gettext(ERREUR_TEXTE).format(pref_file, err.strerror))

    window.set_realtime(prefs.realtime)

    # Message d'accueil
    window.dialog(gettext(INTRO_TEXTE))

    carte = Carte(64, 128)
    carte.generer_salles()
    carte.ajouter_monstres(prefs.difficulty)

    view = VueCarte(carte)

    depart = carte.salles[0]
    col, lig = depart.centre()
    joueur = Joueur(lig, col)
    carte.entities.append(joueur)
    ith = ITH(window, prefs.ith)

    view.center(joueur, window)

    while not window.should_close:
        carte.update_visible(joueur)
        if joueur.vie < 0:
            window.dialog('Game over !')
            break

        carte.update()

        view.refresh(joueur, window)
        ith.refresh(joueur)
        window.refresh()

        if window.resized:
            view = VueCarte(carte)
            view.refresh(joueur, window)
            ith = ITH(window, prefs.ith)
            ith.refresh(joueur)

        if window.open_preferences:
            update_preferences(prefs, pref_file, window)
            window.set_realtime(prefs.realtime)

        if window.moving:
            joueur.deplacer(carte, window.moving)

        if window.shooting:
            joueur.shoot(carte)

    window.close()


if __name__ == "__main__":
    main()
