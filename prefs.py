# -*- coding: utf-8 -*-
""" Gestion des préférences utilisateur """
from sys import stderr
from gettext import gettext

## @enum Difficulté
# La difficulté influe sur le nombre et l'intelligence des monstres
EASY = 0
NORMAL = 1
HARD = 2


class Preferences:
    """ Préférences utilisateur """
    def __init__(self, realtime=False, difficulty=NORMAL, ith=False):
        """ Initialise les préférences. Les champs non renseignés prennent
        les valeurs par défaut """
        ## indique si le jeu
        # attend une action du joueur avant de se mettre à jour
        self.realtime = realtime
        ## la difficulté influe sur le nombre et le type des monstres
        self.difficulty = difficulty
        ## type d'affichage pour l'ITH
        self.ith = ith

    def save(self, filename):
        """ Écrit les préférences dans un fichier :filename:.
        En cas d'erreur renvoie `False` et affiche le message sur `stderr` """
        try:
            with open(filename, "w") as fichier:
                fichier.write("realtime:" + str(self.realtime) + "\n")
                fichier.write("difficulty:" + str(self.difficulty) + "\n")
                fichier.write("ith:" + str(self.ith) + "\n")
            return True
        except OSError as err:
            stderr.write(str(err))
            return False

    def restore(self, filename):
        """ Lit les préférences depuis un fichier :filename:
            Peut lever OSError """
        with open(filename, "r") as fichier:
            for ligne in fichier:
                try:
                    clef, valeur = ligne.split(":")
                except ValueError:  # ligne invalide
                    clef, valeur = "", ""
                try:
                    if clef == "realtime":
                        self.realtime = (valeur == "True\n")
                    elif clef == "difficulty":
                        self.difficulty = int(valeur)
                    elif clef == "ith":
                        self.ith = int(valeur)
                    else:
                        stderr.write(
                            gettext("Attention: préférence inconnue {}\n").
                            format(clef))
                except ValueError:
                    stderr.write(
                        gettext(
                            "Attention: Valeur invalide pour la préférence {}\n"
                        ).format(clef))
