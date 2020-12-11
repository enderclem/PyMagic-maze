# Contient les fonctions calculatoires.

import upemtk as utk
import levels as lvl
import display
import time
import timer

has_stolen = False
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

        if case_target not in ("wall", "unexplored") \
        and new_pos not in lvl.pion_pos \
        and trajectory_target != "wall":
            return True

    return False    


def check_exit():
    """
    Retourne True si tous les joueurs ont atteint la sortie.
    :return bool:
    """
    global reason_stop

    if lvl.has_stolen:
        for i in range(len(lvl.pion_pos)):
            case = lvl.level[lvl.pion_pos[i][1]][lvl.pion_pos[i][0]]
            if lvl.meanings[case] != "exit " + lvl.pion_name[i]:
                return False

        reason_stop = "win"
        return True


def check_hourglass_case(pos):
    """
    Vérifie si la case indiquée est un sablier
    """
    mean=lvl.meanings[lvl.level[pos[1]][pos[0]]]

    if mean=="flip hourglass" and pos not in lvl.deactive_hourglass:
        lvl.discussing=True
        lvl.deactive_hourglass.append(pos)
        timer.flip_timer()
        display.display_timer_X(case=pos)
        for i in range(4):
            display.display_pion(i)
        display.display_discuss(x=10, y=130)


def check_steal():
    """
    Regarde si les objets on été volés
    """
    for i in range(len(lvl.pion_pos)):
        case = lvl.level[lvl.pion_pos[i][1]][lvl.pion_pos[i][0]]
        if lvl.meanings[case] != "to steal " + lvl.pion_name[i]:
            return None

    lvl.has_stolen = True
    display.display_X_vortex()

def check_timer():
    global reason_stop

    if timer.timer<=0:
        reason_stop="lose"
        return True

    return False


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
    elif action=="vortex" and not lvl.has_stolen:
        player_vortex(p)
    elif action=="escalator":
        player_escalator(p)
    elif action=="explore":
        player_explore(p)
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
        display.display_pion(pion)

        check_hourglass_case(new_pos)


def player_explore(p):
    pion=lvl.selected_pion[p]
    pion_name=lvl.pion_name[pion]
    case_pos=lvl.pion_pos[pion]
    case=lvl.level[case_pos[1]][case_pos[0]]
    case_mean=lvl.meanings[case]

    if case_mean=="explore "+pion_name:
        if 1<case_pos[0]<len(lvl.level[0])-2 and 1<case_pos[1]<len(lvl.level)-2:
            # Verifier aussi si ca ne sort pas du terrain
            case_around={"x": {-1: lvl.meanings[lvl.level[case_pos[1]][case_pos[0]-2]],
                               1: lvl.meanings[lvl.level[case_pos[1]][case_pos[0]+2]]}, 
                        "y": {-1: lvl.meanings[lvl.level[case_pos[1]-2][case_pos[0]]],
                               1: lvl.meanings[lvl.level[case_pos[1]+2][case_pos[0]]]}}

            # Calcul de la position de la tuile à poser
            tile_pos_x=case_pos[0] \
                      +(case_around["x"][-1]=="unexplored")*-9 \
                      +(case_around["x"][1] =="unexplored")*1 \
                      +(case_around["y"][-1]=="unexplored")*-3 \
                      +(case_around["y"][1] =="unexplored")*-5
            tile_pos_y=case_pos[1] \
                      +(case_around["x"][-1]=="unexplored")*-5 \
                      +(case_around["x"][1] =="unexplored")*-3 \
                      +(case_around["y"][-1]=="unexplored")*-9 \
                      +(case_around["y"][1] =="unexplored")*1
            # verifier si la tuile sort du terrain
            if 0<=tile_pos_x<=len(lvl.level[0])-9 and 0<=tile_pos_y<=len(lvl.level)-9:
                lvl.add_tile(tile_pos_x, tile_pos_y)

        lvl.level[case_pos[1]][case_pos[0]]=" "
        display.display_all_level()


def player_vortex(p):
    pion=lvl.selected_pion[p]
    pion_name=lvl.pion_name[pion]
    case_pos=lvl.pion_pos[pion]
    case=lvl.level[case_pos[1]][case_pos[0]]
    case_mean=lvl.meanings[case]

    if case_mean=="vortex "+pion_name:
        lvl.player_using_vortex=p
        lvl.selected_vortex=lvl.pion_pos[lvl.selected_pion[p]]
        display.display_selected_vortex()


def player_escalator(p):
    pion=lvl.selected_pion[p]
    case_pos=lvl.pion_pos[pion]
    case=lvl.level[case_pos[1]][case_pos[0]]
    case_mean=lvl.meanings[case]

    if case_mean=="escalator":
        lvl.pion_pos[pion]=lvl.escalator[lvl.pion_pos[pion]]
        display.display_pion(pion)


def selection_change(touche, actual_selection):
    """
    Change la sélection du pion.
    """
    if touche == "b":
        actual_selection += 1
        if actual_selection > 3:
            actual_selection = 0

    # display.display_selected_pion(5, 140, actual_selection)
    return actual_selection


def vortex_selection(input):
    """
    Gère la sélection et l'utilisation du vortex.
    """
    p=lvl.player_using_vortex
    control=lvl.controller[p]
    vort=lvl.selected_vortex
    pion_name=lvl.pion_name[lvl.selected_pion[p]]

    if input in control.keys():
        if "select" in control[input]:
            select_delta=int(control[input].replace("select player ", "").replace("select action ", ""))

            y_start=vort[1]
            y_end=len(lvl.level)*(select_delta==1) - (select_delta==-1)
            x_start=vort[0]+select_delta*2
            x_end=len(lvl.level[0])*(select_delta==1) - (select_delta==-1)

            for y in range(y_start, y_end, select_delta*2):
                for x in range(x_start, x_end, select_delta*2):
                    if lvl.meanings[lvl.level[y][x]] == "vortex "+pion_name:

                        lvl.selected_vortex=(x, y)
                        display.display_selected_vortex()
                        return None

                x_start=(len(lvl.level[0])-1)*(select_delta==-1) + select_delta


        elif control[input]=="do action":
            lvl.player_using_vortex=-1
            lvl.pion_pos[lvl.selected_pion[p]]=vort
            display.efface_selected_vortex()
            display.display_pion(lvl.selected_pion[p])
            
