# -*- coding: utf-8 -*-
""" Affichage tête-haute """

from gettext import gettext

ITH_FIELDS = ["❤︎ Vie", "* Mana", "$ Or"]
ITH_NUMBER_FIELD_LENGTH = 7  # 2*3 chiffres + 1 slash


class ITH:
    def __init__(self):
        """ Précalcul des positions où afficher les champs """
        pass

    def refresh(self, joueur):
        """ Mise à jour de l'affichage """
        pass
