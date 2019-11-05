# -*- coding: utf-8 -*-

import curses
from gettext import gettext

from carte import SYMBOLE_MUR
from joueur import NORTH, SOUTH, WEST, EAST, POISON, CURSE


class Window:
    """ Fenêtre dans le terminal """

    def __init__(self):
        """ Initialisation des ressources """
        self.scr = curses.initscr()
        self.scr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # HP
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Mana
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Or
        curses.init_pair(4, curses.COLOR_BLACK,
                         curses.COLOR_GREEN)  # Empoisonné
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Maudit
        curses.init_pair(6, curses.COLOR_MAGENTA,
                         curses.COLOR_GREEN)  # Poison & maudit

        self.moving = 0
        self.shooting = False

    def refresh(self):
        """ Gestion des événements """
        self.scr.refresh()

        key = self.scr.getch()

        self.moving = 0
        self.shooting = False
        if key == curses.KEY_UP:
            self.moving |= NORTH
        elif key == curses.KEY_DOWN:
            self.moving |= SOUTH
        if key == curses.KEY_LEFT:
            self.moving |= WEST
        elif key == curses.KEY_RIGHT:
            self.moving |= EAST
        elif key == ord('a'):
            self.shooting = True
        elif key == ord('q') or key == 27:  # Escape
            exit()

    def affiche_ith(self, joueur):
        """ Affiche l'interface tête haute pour le :joueur: """
        self.scr.addstr(curses.LINES - 1, 0, ' ' * (curses.COLS - 1))
        self.scr.refresh()
        col = 0

        ith = [
            gettext('❤︎ Vie {}/{} ').format(joueur.vie, joueur.max_vie),
            gettext(' ❇︎ Mana {}/{} ').format(joueur.mana, joueur.max_mana),
            gettext(' $ Or {} ').format(joueur.gold)
        ]

        for i, string in enumerate(ith):
            self.scr.addstr(curses.LINES - 1, col, string,
                            curses.color_pair(i + 1) | curses.A_BOLD)
            col += len(string)

        try:
            self.scr.addstr(
                curses.LINES - 1, col,
                gettext(
                    ' < ^ v > déplacement | a attaque | b parade | p ramasser')
            )
        except:
            # Terminal trop petit!
            pass


def dialog(texte):
    """ Affiche une boîte de dialogue contenant :texte: """
    lignes = texte.split("\n")
    largeur = max(map(len, lignes)) + 3
    hauteur = len(lignes) + 2

    frame = curses.newwin(hauteur, largeur, curses.LINES // 2 - hauteur // 2,
                          curses.COLS // 2 - largeur // 2)
    win = curses.newwin(hauteur - 2, largeur - 2,
                        curses.LINES // 2 - hauteur // 2 + 1,
                        curses.COLS // 2 - largeur // 2 + 1)

    try:
        frame.border()
        win.addstr(texte)
    except curses.error:
        # Votre terminal est trop petit !
        pass
    frame.refresh()

    key = win.getstr()
    if key == chr(27):  # Echap
        sys.exit(0)
    frame.clear()
    frame.refresh()


class VueCarte:
    """ Affichage de la carte """
    def __init__(self, carte):
        self.carte = carte

        self.pad = curses.newpad(carte.hauteur + 1, carte.largeur + 1)

        self.lig_scroll = 0
        self.col_scroll = 0


    def refresh(self, joueur):
        """ Affiche la carte sur un écran ncurses :scr: """
        # Scrolling
        carte = self.carte
        if joueur.lig - self.lig_scroll <= 1 and self.lig_scroll > 0:
            self.lig_scroll -= 1
        elif joueur.lig - self.lig_scroll >= curses.LINES - 2 and self.lig_scroll <= carte.hauteur - curses.LINES:
            self.lig_scroll += 1

        if joueur.col - self.col_scroll <= 1 and self.col_scroll > 0:
            self.col_scroll -= 1
        elif joueur.col - self.col_scroll >= curses.COLS - 2 and self.col_scroll <= carte.largeur - curses.COLS:
            self.col_scroll += 1

        for lig in range(carte.hauteur):
            for col in range(carte.largeur):
                attr = curses.A_NORMAL
                if carte.cases[lig][col] == SYMBOLE_MUR:
                    attr = curses.A_REVERSE
                if carte.cases[lig][col] == '❇︎':
                    attr = curses.color_pair(2)
                self.pad.addstr(lig, col, carte.cases[lig][col], attr)

        # Affichage du joueur
        attr = curses.A_REVERSE
        if joueur.aliment == POISON:
            attr = curses.color_pair(4)
        elif joueur.aliment == CURSE:
            attr = curses.color_pair(5)
        elif joueur.aliment == POISON | CURSE:
            attr = curses.color_pair(6)

        self.pad.addstr(joueur.lig, joueur.col, '@', attr)

        # On laisse la derinière ligne pour l'ITH
        self.pad.refresh(self.lig_scroll, self.col_scroll, 0, 0,
                         curses.LINES - 2, curses.COLS - 1)

    def center(self, joueur):
        """ On centre l'écran sur le joueur """
        self.lig_scroll = joueur.lig - curses.LINES // 2
        self.col_scroll = joueur.col - curses.COLS // 2
