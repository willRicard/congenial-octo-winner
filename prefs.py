# -*- coding: utf-8 -*-
""" Gestion des préférences utilisateur """
from sys import stderr

EASY = 0
NORMAL = 1
HARD = 2


class Preferences:
    """ Préférences utilisateur """
    def __init__(self, realtime=False, difficulty=NORMAL):
        """ Initialise les préférences. Les champs non renseignés prennent
        les valeurs par défaut. """
        self.realtime = realtime
        self.difficulty = difficulty

    def save(self, filename):
        """ Écrit les préférences dans un fichier :filename:.
        En cas d'erreur renvoie `False` et affiche le message sur `stderr`. """
        try:
            with open(filename, "w") as fichier:
                fichier.write("realtime:" + str(self.realtime) + "\n")
                fichier.write("difficulty:" + str(self.difficulty) + "\n")
            return True
        except OSError as err:
            stderr.write(str(err))
            return False

    def restore(self, filename):
        """ Lit les préférences depuis un fichier :filename:
            Peut lever OSError. """
        with open(filename, "r") as fichier:
            for ligne in fichier:
                clef, valeur = ligne.split(":")
                if clef == "realtime":
                    self.realtime = (valeur == "True\n")
                elif clef == "difficulty":
                    self.difficulty = int(valeur)
                else:
                    stderr.write(
                        "Warning: Unknown preference key {}".format(clef) +
                        "\n")
