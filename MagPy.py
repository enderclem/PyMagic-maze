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


def check_guard(name, new_pos):
    enemies=None
    if "garde" in name:
        enemies=("magicienne", "elfe", "nain", "barbare")
    else:
        enemies=tuple(["garde_"+str(i) for i in range(lvl.nbr_guards)])

    for pion in range(len(lvl.pion_pos)):
        if lvl.pion_name[pion] in enemies \
        and lvl.tiles_pos[new_pos]==lvl.tiles_pos[lvl.pion_pos[pion]]:
            return False

    return True


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
    Vérifie si la case indiquée est un sablier^et active l'effet si c'est le cas.
    """
    mean=lvl.meanings[lvl.level[pos[1]][pos[0]]]

    if mean=="flip hourglass" and pos not in lvl.deactive_hourglass:
        lvl.discussing=True
        spell_end_effects()
        lvl.deactive_hourglass.append(pos)
        timer.flip_timer()
        display.display_timer_X(case=pos)
        for i in range(4):
            display.display_pion(i)
        display.display_discuss(x=10, y=130)



def check_steal(input=None):
    """
    Regarde si les objets on été volés
    """
    for i in range(len(lvl.pion_pos)):
        case = lvl.level[lvl.pion_pos[i][1]][lvl.pion_pos[i][0]]
        if lvl.meanings[case] != "to steal " + lvl.pion_name[i] and input!="F12":
            return None

    lvl.has_stolen = True
    # display.display_X_vortex()
    """for y in range(len(lvl.level)):
        for x in range(len(lvl.level[y])):
            if lvl.meanings[lvl.level[y][x]]=="reinforcement unactivated":
                lvl.level[y][x]=lvl.meanings_reverse["reinforcement activated"]
                lvl.pion_pos.append((x, y))
                lvl.pion_name.append("garde")"""
    lvl.add_guards()
    #for pion in range(len(lvl.pion_name)):
     #   display.display_pion(pion)
    display.display_all_level()

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
                good=False
                while not good:
                    lvl.selected_pion[p]+=selection_delta
                    if lvl.selected_pion[p]>=len(lvl.pion_name):
                        lvl.selected_pion[p]=0
                    elif lvl.selected_pion[p]<0:
                        lvl.selected_pion[p]=len(lvl.pion_name)-1
                    if "grenouille" not in lvl.pion_name[lvl.selected_pion[p]]:
                        good=True

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
    elif "spell" in action:
        player_spell(p, action)
    else:
        print("Cette action n'a pas d'effet assigné.")
    # Ajouter ici si l'action est un vortex, escalator...


def player_move(direction, pion):
    """
    Bouge le joueur 1 selon la touche indiquée.
    """
    pion_pos = lvl.pion_pos[pion]  # Création d'un raccourci pour appeler la position du personnage

    vec_move_x = (direction == "right")*2 - (direction == "left")*2
    vec_move_y = (direction == "down")*2 - (direction == "up")*2
    new_pos = (pion_pos[0] + vec_move_x, pion_pos[1] + vec_move_y)

    if check_collision(pion_pos, new_pos) and check_guard(lvl.pion_name[pion], new_pos):
        lvl.pion_pos[pion] = new_pos
        display.display_pion(pion)

        check_hourglass_case(new_pos)


def player_explore(p):
    pion=lvl.selected_pion[p]
    pion_name=lvl.pion_name[pion]
    case_pos=lvl.pion_pos[pion]
    case=lvl.level[case_pos[1]][case_pos[0]]
    case_mean=lvl.meanings[case]
    info=lvl.explore_info(case_pos)

    if case_mean=="explore "+pion_name and info is not None:
        tile_pos=info[0]
        rotation=info[1]
        lvl.add_tile(tile_pos[0], tile_pos[1], rotation)

        lvl.level[case_pos[1]][case_pos[0]]=" "
        display.display_all_level()


def player_spell(p, spell):
    spell=spell.replace("spell_", "")

    if spell=="balai" and len(lvl.deactive_hourglass)!=0:
        lvl.player_using_spell=p
        lvl.spell_being_used=spell
        lvl.selected_spell_target=lvl.deactive_hourglass[0]
        display.display_selected_target(lvl.selected_spell_target)
    if spell=="grenouille" and any(filter(lambda name: "garde" in name, lvl.pion_name)): # Vérifie si un garde existe
        lvl.player_using_spell=p
        lvl.spell_being_used=spell
        for i in range(len(lvl.pion_name)):
            if "garde" in lvl.pion_name[i]:
                lvl.selected_spell_target=lvl.pion_pos[i]
                break
        display.display_selected_target(lvl.selected_spell_target)

    else:
        print("Le sort utilisé n'est pas assigné ou ne peut pas être utilisé maintenant.")


def player_vortex(p):
    pion=lvl.selected_pion[p]
    pion_name=lvl.pion_name[pion]
    case_pos=lvl.pion_pos[pion]
    case=lvl.level[case_pos[1]][case_pos[0]]
    case_mean=lvl.meanings[case]

    if case_mean=="vortex "+pion_name:
        lvl.player_using_vortex=p
        lvl.selected_vortex=lvl.pion_pos[lvl.selected_pion[p]]
        display.display_selected_target(lvl.selected_vortex)


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

    return actual_selection


def spell_end_effects():
    """Met fin aux effets temporaires des sorts."""
    for i in range(len(lvl.pion_name)):
        if "grenouille" in lvl.pion_name[i]:
            lvl.pion_name[i] = "garde_" + lvl.pion_name[i].split("_")[1]
            display.display_pion(i)

    
def spell_target_selection(input):
    spell=lvl.spell_being_used
    p=lvl.player_using_spell
    control=lvl.controller[p]
    target=lvl.selected_spell_target

    if input in control.keys():
        if "select" in control[input]:
            select_delta=int(control[input].replace("select player ", "").replace("select action ", ""))

            # Sélection pour le sort balai
            if spell=="balai":
                target_id=lvl.deactive_hourglass.index(target)
                target_id+=select_delta
                if target_id>=len(lvl.deactive_hourglass):
                    target_id=0
                lvl.selected_spell_target=lvl.deactive_hourglass[target_id]
                display.display_selected_target(lvl.selected_spell_target)

            # Sélection durant le sort grenouille
            if spell=="grenouille":
                target_id=lvl.pion_pos.index(target)
                while True:
                    target_id+=select_delta
                    if target_id>=len(lvl.pion_name):
                        target_id=0
                    if target_id<0:
                        target_id=len(lvl.pion_name)-1
                    if "garde" in lvl.pion_name[target_id]:
                        lvl.selected_spell_target=lvl.pion_pos[target_id]
                        break
                display.display_selected_target(lvl.selected_spell_target)

        elif control[input]=="do action":
            # Effet du sort balai
            if spell=="balai":
                lvl.player_using_spell=-1
                lvl.deactive_hourglass.remove(target)
                utk.efface("X_"+str(target[0])+"_"+str(target[1]))
                display.efface_selected_target()
                for p in range(len(lvl.players_act)):
                    print("Nom du sort utilisé :", "spell_"+str(spell))
                    lvl.players_act[p].remove("spell_"+str(spell))

            # Effet du sort grenouille
            if spell=="grenouille":
                lvl.player_using_spell=-1
                target_id=lvl.pion_pos.index(target)
                # utk.efface("pion"+str(target_id))
                lvl.pion_name[target_id] = "grenouille_" + lvl.pion_name[target_id].split("_")[1]
                display.display_pion(target_id)
                display.efface_selected_target()
                for p in range(len(lvl.players_act)):
                    print("Nom du sort utilisé :", "spell_"+str(spell))
                    lvl.players_act[p].remove("spell_"+str(spell))


def vortex_selection(input):
    """
    Gère la sélection et l'utilisation du vortex.
    """
    p=lvl.player_using_vortex
    control=lvl.controller[p]
    vort=lvl.selected_vortex
    pion=lvl.selected_pion[p]
    pion_name=lvl.pion_name[pion]
    pion_pos_others=lvl.pion_pos[0:pion]+lvl.pion_pos[pion+1:len(lvl.pion_pos)]

    if input in control.keys():
        if "select" in control[input]:
            select_delta=int(control[input].replace("select player ", "").replace("select action ", ""))

            y_start=vort[1]
            y_end=len(lvl.level)*(select_delta==1) - (select_delta==-1)
            x_start=vort[0]+select_delta*2
            x_end=len(lvl.level[0])*(select_delta==1) - (select_delta==-1)

            for y in range(y_start, y_end, select_delta*2):
                for x in range(x_start, x_end, select_delta*2):
                    if lvl.meanings[lvl.level[y][x]] == "vortex "+pion_name and check_guard(pion_name, (x, y)) and (x, y) not in pion_pos_others:
                        lvl.selected_vortex=(x, y)
                        display.display_selected_target(lvl.selected_vortex)
                        return None

                x_start=(len(lvl.level[0])-1)*(select_delta==-1) + select_delta


        elif control[input]=="do action":
            lvl.player_using_vortex=-1
            lvl.pion_pos[lvl.selected_pion[p]]=vort
            display.efface_selected_target()
            display.display_pion(lvl.selected_pion[p])

