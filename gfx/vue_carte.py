# -*- coding: utf-8 -*-
""" Affichage de la carte """
import curses

from entity import ALIMENT_POISON, ALIMENT_CURSE
from joueur import Joueur

from monstre.rat import Rat
from monstre.goblin import Goblin

from gfx.window import COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_MAGENTA, COLOR_GREEN_MAGENTA

## @enum Symbole
# Caractère utilisé pour l'affichage
SYMBOLE_JOUEUR = '@'  # caractère affiché à la position des joueurs
SYMBOLE_PROJECTILE = '*'  # caractère affiché à la position des projectiles
SYMBOLE_SOL = '.'  # caractère affiché sur une case libre
SYMBOLE_MUR = '#'  # caractère affichée sur une case occupée
SYMBOLE_RAT = 'r'  # caractère affiché à la position des rats
SYMBOLE_GOBLIN = 'X'  # caractère affiché à la poisition des goblins


class VueCarte:
    """ Affichage de la carte """
    def __init__(self, carte):
        """ Constructeur """
        ## Référence vers la carte
        self.carte = carte

        ## Fenêtre glissante pour l'affichage
        self.pad = curses.newpad(carte.hauteur + 1, carte.largeur + 1)

        ## Ordonnée du coin supérieur gauche de la vue affichée
        self.lig_scroll = 0
        ## Abscisse du coin supérieur gauche de la vue affichée
        self.col_scroll = 0

    def refresh(self, joueur, window):
        """ Affiche la carte sur un écran ncurses :scr: """
        # Scrolling
        carte = self.carte
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= window.height - 2 and (
                self.lig_scroll <= carte.hauteur - window.height):
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll -= 1
        elif joueur.col - self.col_scroll >= window.width - 2 and (
                self.col_scroll <= carte.largeur - window.width):
            self.col_scroll += 1

        # Affichage de la carte
        for lig in range(carte.hauteur):
            for col in range(carte.largeur):
                if carte.cases[lig] & 1 << col:
                    self.pad.addstr(lig, col, SYMBOLE_SOL)
                else:
                    self.pad.addstr(lig, col, SYMBOLE_MUR, curses.A_REVERSE)

        # Affichage des projectiles
        for projectile in carte.projectiles:
            self.pad.addstr(projectile.lig, projectile.col, SYMBOLE_PROJECTILE,
                            curses.color_pair(COLOR_BLUE))

        self.draw_entities(carte.entities)

        # On laisse la derinière ligne pour l'ITH
        self.pad.refresh(self.lig_scroll, self.col_scroll, 0, 0,
                         window.height - 2, window.width - 1)

    def draw_entities(self, entities):
        """ Affichage des monstres et des joueurs """
        for entity in entities:
            symbole = SYMBOLE_GOBLIN
            attr = curses.A_NORMAL

            if isinstance(entity, Rat):
                symbole = SYMBOLE_RAT
                attr |= curses.color_pair(COLOR_RED)
            elif isinstance(entity, Goblin):
                symbole = SYMBOLE_GOBLIN
                attr |= curses.color_pair(COLOR_RED)
            elif isinstance(entity, Joueur):
                symbole = SYMBOLE_JOUEUR
                attr |= curses.A_REVERSE

            # Les altérations d'état
            # modifient la couleur d'affichage
            if entity.aliment == ALIMENT_POISON:
                attr |= curses.color_pair(COLOR_GREEN)
            elif entity.aliment == ALIMENT_CURSE:
                attr |= curses.color_pair(COLOR_MAGENTA)
            elif entity.aliment == ALIMENT_POISON | ALIMENT_CURSE:
                attr |= curses.color_pair(COLOR_GREEN_MAGENTA)

            try:
                self.pad.addstr(entity.lig, entity.col, symbole, attr)
            except curses.error:
                pass

    def center(self, joueur, window):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - window.height // 2
        self.col_scroll = joueur.col - window.width // 2
