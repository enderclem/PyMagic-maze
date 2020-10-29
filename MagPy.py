# Contient les fonctions calculatoires.

import upemtk as utk
from levels import *
import display

players_input = ("z", "s", "q", "d")

selection_blocked = False

has_stolen = False

def check_steal():
    global has_stolen
    for i in range(len(players_pos)):
        case = level[players_pos[i][1]][players_pos[i][0]]
        if meanings[case] != "to steal " + players_name[i]:
            return None

    has_stolen = True
    display.open_exit()

def check_exit():
    global has_stolen
    if has_stolen:
        for i in range(len(players_pos)):
            case = level[players_pos[i][1]][players_pos[i][0]]
            if meanings[case] != "exit " + players_name[i]:
                return None

        display.display_win()


def move_player(touche, p):
    """
    Bouge le joueur 1 selon la touche indiquée.

    :param string touche: touche du clavier appuyé
    :param int p: numéro du joueur
    """
    global players
    global players_input
    pla = players_pos[p]  # Création d'un raccourci pour appeler la position du personnage

    vec_move_x = (touche == players_input[3]) - (touche == players_input[2])
    vec_move_y = (touche == players_input[1]) - (touche == players_input[0])
    new_pos = (pla[0] + vec_move_x, pla[1] + vec_move_y)

    if -1 < new_pos[1] < len(level) and -1 < new_pos[0] < len(level[0]) \
            and level[new_pos[1]][new_pos[0]] != "w" \
            and new_pos not in players_pos:
        players_pos[p] = new_pos

    display.display_player(p)

def selection_change(touche, actual_selection):
    """
    Change la sélection du pion.

    :param string input: Valeur de la touche appuyé
    :param int actual_selection: Numéro du pion actuellement sélectionné
    :return: retourne la nouvelle valeur du pion séléctionné
    """
    global selection_blocked
    if touche == "v":
        selection_blocked = not selection_blocked

    if touche == "e" and not selection_blocked:
        actual_selection += 1
        if actual_selection > 3:
            actual_selection = 0

    return actual_selection
