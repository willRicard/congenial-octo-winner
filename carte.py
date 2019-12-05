# -*- coding: utf-8 -*-
""" Tableau 2D de caractères """
from random import random, randrange, choice, choices

from rect import Rect

from monstre.monstre import Monstre, SPAWN_RATE
from monstre.rat import Rat
from monstre.goblin import Goblin
from projectile import Projectile

NUM_SALLES = 10
PROBA_ARRET = 0.2
PROBA_GRANDE_SALLE = 0.2
EPAISSEUR_MUR = 1


class Carte:
    """ Une carte de caractères """
    def __init__(self, hauteur=100, largeur=100):
        self.hauteur = hauteur
        self.largeur = largeur

        self.cases = [0 for lig in range(hauteur)]

        self.salles = []

        self.entities = []

        self.projectiles = []

    def relier(self, depart, arrivee):
        """ Couloir entre :depart: et :arrivee:
        Requiert deux cellules sur la même ligne ou la même colonne. """
        vertical = (depart[0] == arrivee[0])
        if vertical:
            col = depart[0]
            for lig in range(min(depart[1], arrivee[1]),
                             max(depart[1], arrivee[1]) + 1):
                self.cases[lig] |= 1 << col
        else:
            lig = depart[1]
            for col in range(min(depart[0], arrivee[0]),
                             max(depart[0], arrivee[0]) + 1):
                self.cases[lig] |= 1 << col

    def partitionner(self, salle, depth=0):
        """ Découpe une salle en quatre """
        # Condition d'arrêt: arrêt aléatoire ou salle trop petite
        if salle.width <= 10 or salle.height <= 10:
            self.salles.append(salle)
            return []

        w_max = salle.width // 3
        h_max = salle.height // 3
        x_split = randrange(w_max, salle.width - w_max)
        y_split = randrange(h_max, salle.height - h_max)

        enfants = [
            # Haut gauche
            Rect(salle.left, salle.top, x_split, y_split, depth=depth),
            # Haut droite
            Rect(salle.left + x_split + EPAISSEUR_MUR,
                 salle.top,
                 salle.width - x_split - 2 * EPAISSEUR_MUR,
                 y_split,
                 depth=depth),
            # Bas gauche
            Rect(salle.left,
                 salle.top + y_split + EPAISSEUR_MUR,
                 x_split,
                 salle.height - y_split - 2 * EPAISSEUR_MUR,
                 depth=depth),
            # Bas droite
            Rect(salle.left + x_split + EPAISSEUR_MUR,
                 salle.top + y_split + EPAISSEUR_MUR,
                 salle.width - x_split - 2 * EPAISSEUR_MUR,
                 salle.height - y_split - 2 * EPAISSEUR_MUR,
                 depth=depth)
        ]

        # on copie pour enlever
        # des éléments sans
        # casser la boucle
        for enfant in list(enfants):
            # profondeur suivante
            if random() > PROBA_ARRET + PROBA_GRANDE_SALLE:
                self.partitionner(enfant, depth=depth + 1)
            # pas de salle
            elif random() < PROBA_ARRET:
                enfants.remove(enfant)
            # grande salle
            else:
                self.salles.append(enfant)

        # On relie les salles
        # pour qu'elles soient
        # toutes atteignables
        for enfant in enfants:
            self.relier(salle.centre(),
                        enfant.centre())  # on relie chaque salle à son parent
            autre = choice(enfants)
            oops = 0
            while autre == enfant and oops <= 1000:
                autre = choice(enfants)
                oops += 1
            self.relier(enfant.centre(), autre.centre())

        return enfants

    def generer_salles(self):
        """ Genere les salles par une approche récursive """
        # on laisse un mur autour du donjon
        donjon = Rect(1, 1, self.largeur - 2, self.hauteur - 2)

        self.partitionner(donjon)

        for salle in self.salles:
            for lig in range(salle.top, salle.top + salle.height):
                for col in range(salle.left, salle.left + salle.width):
                    self.cases[lig] |= 1 << col

    def ajouter_monstres(self, difficulte):
        """ Ajoute des monstres en tenant compte de la :difficulte: """
        num_monstres = [3, 2, 1]
        # on ajoute pas de monstres dans la salle de départ
        for salle in self.salles[1:]:
            for _ in range(num_monstres[salle.depth]):
                col, lig = salle.centre()
                col += randrange(0, 4)
                lig += randrange(0, 4)
                classe_monstre = choices([Rat, Goblin],
                                         weights=SPAWN_RATE[difficulte])[0]
                self.entities.append(classe_monstre(self, lig, col))

    def ajouter_projectile(self, joueur):
        """ Ajoute un projectile aux coordonnées :lig: :col: se déplaçant dans la :direction:
            Rien ne se passe si la case est occupée. """
        if self.case_libre(joueur.lig, joueur.col):
            self.projectiles.append(
                Projectile(joueur, joueur.lig, joueur.col, joueur.facing))

    def update(self):
        """ Met à jour le joueur, les monstres et les projectiles """
        for projectile in self.projectiles.copy():
            projectile.update()
            for monstre in filter(lambda x: isinstance(x, Monstre),
                                  self.entities.copy()):
                if (projectile.lig, projectile.col) == (monstre.lig,
                                                        monstre.col):
                    monstre.vie -= 1
                    if monstre.vie == 0:
                        # le joueur gagne l'or du monstre
                        projectile.parent.gold += monstre.gold
                        self.entities.remove(monstre)
                        self.projectiles.remove(projectile)
            if ~(self.cases[projectile.lig] & 1 << projectile.col) & 1 << projectile.col:
                self.projectiles.remove(projectile)
        for entity in self.entities:
            entity.update()

    def case_libre(self, lig, col):
        """ Renvoie True si la case est libre (ni mur, ni monstre) """
        if lig < 0 or lig > self.hauteur or col < 0 or col > self.largeur or ~(
                self.cases[lig] & 1 << col) & 1 << col:
            return False

        for entity in self.entities:
            if isinstance(entity,
                          Monstre) and lig == entity.lig and col == entity.col:
                return False
        return True

    def voisins(self, lig, col):
        """ Itère sur les cases voisines de (:lig:, :col:). """
        for lig_voisin, col_voisin in [(lig - 1, col), (lig, col - 1),
                                       (lig, col + 1), (lig + 1, col)]:
            if self.case_libre(lig_voisin, col_voisin):
                yield (lig_voisin, col_voisin)
