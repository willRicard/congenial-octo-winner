# -*- coding: utf-8 -*-
""" Entité générique """
from queue import PriorityQueue

from rect import distance


# pylint: disable=too-few-public-methods
class Entity:
    """ Entité générique """
    def __init__(self, lig, col, vie=1, gold=10):
        self.lig = lig  # ordonnée
        self.col = col  # abscisse
        self.vie = vie  # points de vie
        self.max_vie = vie  # conservé pour l'affichage
        self.gold = gold
        self.aliment = 0


def a_etoile(carte, start, goal):
    """ Renvoie le chemin pour aller de :start: jusqu'à :goal: sur la :carte: """
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        new_cost = cost_so_far[current] + 1
        for voisin in carte.voisins(*current):
            if voisin not in cost_so_far or new_cost < cost_so_far[voisin]:
                cost_so_far[voisin] = new_cost
                came_from[voisin] = current
                priority = new_cost + distance(voisin[0], voisin[1], *goal)
                frontier.put(voisin, priority)

    path = []
    while current != start:
        path = [current] + path
        current = came_from[current]
    return path
