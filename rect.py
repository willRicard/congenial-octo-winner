# -*- coding: utf-8 -*-
""" Rectangle """


class Rect:
    """ Rectangle 2D """
    def __init__(self, left, top, width, height, depth=0):
        """ Constructeur """
        ## Abscisse du coin supérieur gauche
        self.left = left
        ## Ordonnée du coin supérieur gauche
        self.top = top
        ## Largeur
        self.width = width
        ## Hauteur
        self.height = height
        ## Profondeur de la salle
        self.depth = depth

        ## Précalcul du centre
        self.point_centre = (self.left + self.width // 2,
                             self.top + self.height // 2)

    def centre(self):
        """ Retourne les coordonées du centre """
        return self.point_centre

    def bounds(self, other):
        """ Renvoie le plus petit rectangle qui contienne :self: et :other: """
        return Rect(
            min(self.left, other.left), min(self.top, other.top),
            self.width + other.width + other.left - self.left - self.width,
            self.height + other.height + other.top - self.top - self.height)

    def contains(self, x_point, y_point):
        """ Renvoie True si le point (:x_point:, :y_point:) appartient au rectangle """
        return self.left <= x_point <= self.left + self.width and (
            self.top <= y_point <= self.top + self.height)


def distance(lig1, col1, lig2, col2):
    """ Renvoie la distance entre deux cellules """
    return abs(lig2 - lig1) + abs(col2 - col1)
