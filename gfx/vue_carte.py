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

# Caractère affiché à la position des joueurs
SYMBOLE_JOUEUR = '@'
## Caractère affiché à la position des projectiles
SYMBOLE_PROJECTILE = '*'
## Caractère affiché sur une case libre
SYMBOLE_SOL = '.'
## Caractère affichée sur une case occupée
SYMBOLE_MUR = '#'
## Caractère affiché à la position des rats
SYMBOLE_RAT = 'r'
## Caractère affiché à la poisition des goblins
SYMBOLE_GOBLIN = 'X'


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
        for lig in range(self.lig_scroll,
                         min(self.lig_scroll + window.height, carte.hauteur)):
            for col in range(
                    self.col_scroll,
                    min(self.col_scroll + window.width, carte.largeur)):
                if carte.visible[lig] & 1 << col:
                    if carte.cases[lig] & 1 << col:
                        self.pad.addstr(lig, col, SYMBOLE_SOL)
                    else:
                        self.pad.addstr(lig, col, SYMBOLE_MUR,
                                        curses.A_REVERSE)

        # Affichage des projectiles
        for projectile in carte.projectiles:
            lig, col = projectile.lig, projectile.col
            if self.carte.visible[lig] & 1 << col:
                self.pad.addstr(lig, col, SYMBOLE_PROJECTILE,
                                curses.color_pair(COLOR_BLUE))

        self.draw_entities(carte.entities)

        # On laisse la derinière ligne pour l'ITH
        self.pad.refresh(self.lig_scroll, self.col_scroll, 0, 0,
                         window.height - 2, window.width - 1)

    def draw_entities(self, entities):
        """ Affichage des monstres et des joueurs """
        for entity in entities:
            lig, col = entity.lig, entity.col
            if ~(self.carte.visible[lig] & 1 << col) & 1 << col:
                continue

            symbole = SYMBOLE_GOBLIN
            attr = curses.color_pair(COLOR_RED)

            if isinstance(entity, Rat):
                symbole = SYMBOLE_RAT
            elif isinstance(entity, Joueur):
                symbole = SYMBOLE_JOUEUR
                attr = curses.A_REVERSE

            # Les altérations d'état
            # modifient la couleur d'affichage
            if entity.aliment == ALIMENT_POISON:
                attr |= curses.color_pair(COLOR_GREEN)
            elif entity.aliment == ALIMENT_CURSE:
                attr |= curses.color_pair(COLOR_MAGENTA)
            elif entity.aliment == ALIMENT_POISON | ALIMENT_CURSE:
                attr |= curses.color_pair(COLOR_GREEN_MAGENTA)

            self.pad.addstr(entity.lig, entity.col, symbole, attr)

    def center(self, joueur, window):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = max(0, joueur.lig - window.height // 2)
        self.col_scroll = max(0, joueur.col - window.width // 2)
