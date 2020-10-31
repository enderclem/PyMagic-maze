# Contient les fonctions calculatoires.

import upemtk as utk
import levels as lvl
import display
import time

players_input = ("z", "s", "q", "d")
selection_blocked = False
has_stolen = False
last_frame_time = time.time()
reason_stop = "quit"  # Contient une variable pour décider de quoi faire après la fin de la boucle principale

def check_steal():
    """

    :return:
    """
    global has_stolen

    for i in range(len(lvl.players_pos)):
        case = lvl.level[lvl.players_pos[i][1]][lvl.players_pos[i][0]]
        if lvl.meanings[case] != "to steal " + lvl.players_name[i]:
            return None

    has_stolen = True
    display.open_exit()

def check_exit():
    """
    Retourne True si tous les joueurs ont atteint la sortie.
    :return bool:
    """
    global has_stolen
    global reason_stop

    if has_stolen:
        for i in range(len(lvl.players_pos)):
            case = lvl.level[lvl.players_pos[i][1]][lvl.players_pos[i][0]]
            if lvl.meanings[case] != "exit " + lvl.players_name[i]:
                return False

        reason_stop = "win"
        return True

def end_game():
    global reason_stop

    if reason_stop == "quit":
        return None

    if reason_stop == "win":
        display.display_win()

    if reason_stop == "lose":
        display.display_lose()

    time.sleep(1)
    utk.attente_clic_ou_touche()

def move_player(touche, p):
    """
    Bouge le joueur 1 selon la touche indiquée.

    :param string touche: touche du clavier appuyé
    :param int p: numéro du joueur
    """
    global players
    global players_input
    pla = lvl.players_pos[p]  # Création d'un raccourci pour appeler la position du personnage

    vec_move_x = (touche == players_input[3]) - (touche == players_input[2])
    vec_move_y = (touche == players_input[1]) - (touche == players_input[0])
    new_pos = (pla[0] + vec_move_x, pla[1] + vec_move_y)

    if -1 < new_pos[1] < len(lvl.level) and -1 < new_pos[0] < len(lvl.level[0]) \
            and lvl.level[new_pos[1]][new_pos[0]] != "w" \
            and new_pos not in lvl.players_pos:
        lvl.players_pos[p] = new_pos

    display.display_player(p)

def update_time():
    """
    Met à jour le timer et vérifie si le temps est écoulé

    :return bool:
    """
    global last_frame_time
    global reason_stop

    lvl.time_left -= time.time() - last_frame_time
    last_frame_time = time.time()

    if lvl.time_left <= 0:
        reason_stop = "lose"
        return True

    return False

def selection_change(touche, actual_selection):
    """
    Change la sélection du pion.

    :param string input: Valeur de la touche appuyé
    :param int actual_selection: Numéro du pion actuellement sélectionné
    :return: retourne la nouvelle valeur du pion séléctionné
    """
    global selection_blocked
    if touche == "n":
        selection_blocked = not selection_blocked

    if touche == "b" and not selection_blocked:
        actual_selection += 1
        if actual_selection > 3:
            actual_selection = 0

    display.display_selected(420, 10, actual_selection, selection_blocked)
    return actual_selection
