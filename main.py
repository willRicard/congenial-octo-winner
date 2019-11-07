#!/usr/bin/env python
""" Project Python Semestre 1 """
from random import seed, random
from gettext import gettext, bindtextdomain

from carte import Carte
from joueur import Joueur, NORTH, SOUTH, EAST, WEST, POISON, CURSE

from gfx.window import Window, dialog
from gfx.vue_carte import VueCarte
from gfx.ith import ITH

INTRO_TEXTE = gettext("Bienvenue, aventurier !\n\
Vous avez parcouru un long chemin pour arriver ici en quête de gloire.\n\
Vous entrez maintenant dans les donjons d'Eneladim.\n\n\
Pourrez vous faire face aux fléaux de cet endroit?\n\n\
Appuyez sur Échap. pour quitter.\n\
Appuyez sur Entrée pour continuer.")

PROBA_ALTERATION = 0.05


def main():
    """ Point d'entrée du programme """
    # seed(0)
    bindtextdomain("messages", ".")

    window = Window()

    # Message d'accueil
    dialog(INTRO_TEXTE)

    carte = Carte(64, 128)
    carte.generer_salles()

    view = VueCarte(carte)

    # Départ dans une salle aléatoire
    depart = carte.salles[0]
    col, lig = depart.centre()
    joueur = Joueur(lig, col)
    ith = ITH()

    view.center(joueur)

    while True:
        # On inflige une altération d'état aléatoire au joueur
        # avec une certaine probabilité
        if random() < PROBA_ALTERATION:
            if random() < 0.5 and not joueur.aliment & POISON:
                joueur.aliment |= POISON
                dialog(gettext('Les miasmes du donjon vous ont empoisonné !'))
            elif not joueur.aliment & CURSE:
                joueur.aliment |= CURSE
                dialog(gettext('Le donjon absorbe votre énergie magique !'))

        if joueur.vie == 0:
            dialog('Game over !')
            break

        joueur.update()
        carte.update(joueur)

        view.refresh(joueur)
        ith.refresh(joueur)
        window.refresh()

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
