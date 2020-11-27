# Contient les fonctions calculatoires.

import upemtk as utk
import levels as lvl
import display
import time

has_stolen = False
last_frame_time = time.time()
reason_stop = "quit"  # Contient une variable pour décider de quoi faire après la fin de la boucle principale


def check_collision(last_pos, new_pos):
    """
    Renvoie True si le personnage peut aller à la nouvelle position indiquée.
    """

    if -1 < new_pos[1] < len(lvl.level) and -1 < new_pos[0] < len(lvl.level[0]): # Vérifie leslimites du terrain

        direction=((new_pos[0]-last_pos[0])//2, (new_pos[1]-last_pos[1])//2)
        # Pour après vérifier si la nouvelle position se trouve dans un mur
        case_target=lvl.meanings[lvl.level[new_pos[1]][new_pos[0]]]
        # Pour vérifier si on essaie de passer par un mur
        trajectory_target=lvl.meanings[lvl.level[last_pos[1]+direction[1]][last_pos[0]+direction[0]]]

        if case_target != "wall" \
        and new_pos not in lvl.pion_pos \
        and trajectory_target != "wall":
            return True

    return False    


def check_exit():
    """
    Retourne True si tous les joueurs ont atteint la sortie.
    :return bool:
    """
    global has_stolen
    global reason_stop

    if has_stolen:
        for i in range(len(lvl.pion_pos)):
            case = lvl.level[lvl.pion_pos[i][1]][lvl.pion_pos[i][0]]
            if lvl.meanings[case] != "exit " + lvl.pion_name[i]:
                return False

        reason_stop = "win"
        return True

def check_steal():
    """

    :return:
    """
    global has_stolen

    for i in range(len(lvl.pion_pos)):
        case = lvl.level[lvl.pion_pos[i][1]][lvl.pion_pos[i][0]]
        if lvl.meanings[case] != "to steal " + lvl.pion_name[i]:
            return None

    has_stolen = True
    display.open_exit()

def end_game():
    """
    Définit ce qui doit être affiché après avoir quitter le jeu. 
    """
    global reason_stop

    if reason_stop == "quit":
        return None

    if reason_stop == "win":
        display.display_win()

    if reason_stop == "lose":
        display.display_lose()

    time.sleep(1)
    utk.attente_clic_ou_touche()


def player_choose(input):
    """
    Gère l'action à axécuter en fonction de la touche appuyée
    """
    for p in range(lvl.nbr_of_player):
        contr=lvl.controller[p]
        if input in contr.keys():
            mean=contr[input]

            if "select player" in mean:
                selection_delta=int(mean.replace("select player ", ""))
                lvl.selected_pion[p]+=selection_delta
                if lvl.selected_pion[p]>3:
                    lvl.selected_pion[p]=0
                elif lvl.selected_pion[p]<0:
                    lvl.selected_pion[p]=3

            elif "select action" in mean:
                selection_delta=int(mean.replace("select action ", ""))
                lvl.selected_act[p]+=selection_delta
                if lvl.selected_act[p]>=len(lvl.players_act[p]):
                    lvl.selected_act[p]=0
                elif lvl.selected_act[p]<0:
                    lvl.selected_act[p]=len(lvl.players_act[p])-1

            elif mean=="do action":
                player_act(p)


def player_act(p):
    """
    Exécute l'action sélectionnée du joueur en question.
    """
    action=lvl.players_act[p][lvl.selected_act[p]]
    if "go" in action:
        player_move(action.replace("go_", ""), lvl.selected_pion[p])
    # Ajouter ici si l'action est un vortex, escalator...


def player_move(direction, pion):
    """
    Bouge le joueur 1 selon la touche indiquée.
    """
    pion_pos = lvl.pion_pos[pion]  # Création d'un raccourci pour appeler la position du personnage

    vec_move_x = (direction == "right")*2 - (direction == "left")*2
    vec_move_y = (direction == "down")*2 - (direction == "up")*2
    new_pos = (pion_pos[0] + vec_move_x, pion_pos[1] + vec_move_y)

    if check_collision(pion_pos, new_pos):
        lvl.pion_pos[pion] = new_pos


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
    if touche == "b":
        actual_selection += 1
        if actual_selection > 3:
            actual_selection = 0

    # display.display_selected_pion(5, 140, actual_selection)
    return actual_selection
