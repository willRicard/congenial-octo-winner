# -*- coding: utf-8 -*-
""" Entité générique """
from queue import PriorityQueue

from rect import distance

## @enum Direction parmi 8 possibles.
# On utilise un masque pour pouvoir
# se déplacer / tirer en diagonale.
NORTH = 1
SOUTH = 2
WEST = 4
EAST = 8

## @enum Altération d'état
# Malus attribué aux joeurs/monstres
ALIMENT_POISON = 1  # un joueur empoisonné perd progressivement des PV
ALIMENT_CURSE = 2  # un joueur maudit perd progressivement des PM


# pylint: disable=too-few-public-methods,too-many-arguments
class Entity:
    """ Entité générique """
    def __init__(self, lig, col, facing=NORTH, vie=1, gold=10):
        """ Constructeur
        Requiert des coordonées :lig:, :col: valides.
        Requiert :vie: > 0."""
        ## ordonnée
        self.lig = lig
        ## abscisse
        self.col = col
        ## points de vie
        self.vie = vie
        ## conservé pour l'affichage
        self.max_vie = vie
        ## pièces d'or
        self.gold = gold
        ## altération d'état
        self.aliment = 0
        ## direction regardée
        self.facing = facing

    def deplacer(self, carte, direction):
        """ Déplace l'entité sur la :carte: dans la :direction: """
        lig, col = self.lig, self.col

        if direction & NORTH:
            lig -= 1
        elif direction & SOUTH:
            lig += 1
        if direction & WEST:
            col -= 1
        elif direction & EAST:
            col += 1

        if carte.case_libre(lig, col):
            self.lig = lig
            self.col = col

            self.facing = direction


def a_etoile(carte, start, goal):
    """ Renvoie le chemin pour aller de :start:
    jusqu'à :goal: sur la :carte: """
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

    path = [goal]
    while current != start:
        path = [current] + path
        current = came_from[current]
    return path
