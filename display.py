# Contient toutes les fonctions d'affichages.

import upemtk as utk
import levels as lvl
import timer

win_size = (1200, 680)
level_pos = (120, 20)  # Donne la position du coin supérieur gauche de l'affichage du niveau
level_px = (960, 640)  # Taille du niveau en pixel


def display_all_level():
    """
    Réaffiche tous les éléments à la fenêtre.
    """
    global has_stole

    utk.efface_tout()

    utk.rectangle(level_pos[0]-20, level_pos[1]-20, 
                  level_pos[0]+level_px[0]+20, level_pos[1]+level_px[1]+20,
                  couleur="black",
                  remplissage="black",
                  epaisseur=0,
                  tag="background")

    display_cases()
    display_between_cases()
    for i in range(len(lvl.pion_pos)):
        display_pion(i)
    display_selected_game()
    if lvl.player_using_vortex!=-1:
        display_selected_target(lvl.selected_vortex)
    if lvl.player_using_spell!=-1:
        display_selected_target(lvl.selected_spell_target)
    display_escalators()
    if lvl.discussing:
        display_discuss(x=10, y=130)

    utk.mise_a_jour()

def display_between_cases():

    for yy in range(0, len(lvl.level), 2):
        for xx in range(1, len(lvl.level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = lvl.level[yy][xx]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + 20 + level_pos[0], y * 40 + level_pos[1])

            # Affichage des murs
            if lvl.meanings[case] == "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/wall_horizontal.gif")

    for yy in range(1, len(lvl.level), 2):
        for xx in range(0, len(lvl.level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = lvl.level[yy][xx]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + level_pos[0], y * 40 + 20 + level_pos[1])

            # Affichage des murs
            if lvl.meanings[case] == "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/wall_vertical.gif")


def display_cases():
    for yy in range(1, len(lvl.level), 2):
        for xx in range(1, len(lvl.level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = lvl.level[yy][xx]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + 20 + level_pos[0], y * 40 + 20 + level_pos[1])

            # Affichage du sol
            if lvl.meanings[case] not in ("wall", "unexplored"):
                utk.image(case_pos[0], case_pos[1], "sprites/ground.gif")

            # Affichage des zones à voler
            if "to steal" in lvl.meanings[case] and not lvl.has_stolen:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/stuff_" + lvl.meanings[case].replace("to steal ", "") + ".gif", 
                          tag="to_steal")

            # Affichage des sorties
            elif "exit" in lvl.meanings[case]:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/exit_" + lvl.meanings[case].replace("exit ", "") + ".gif")

                if not lvl.has_stolen:
                    utk.image(case_pos[0], case_pos[1],
                              "sprites/X.gif",
                              tag="closed")

            # Affichage des cases sabliers
            elif lvl.meanings[case] == "flip hourglass":
                utk.image(case_pos[0], case_pos[1],
                          "sprites/flip_hourglass.gif")

                if (xx, yy) in lvl.deactive_hourglass:
                    utk.image(case_pos[0], case_pos[1],
                              "sprites/X.gif",
                              tag="X_"+str(xx)+"_"+str(yy))

            # Affichage des cases sabliers
            elif "vortex" in lvl.meanings[case]:
                display_vortex(case_pos, lvl.meanings[case])

                if lvl.has_stolen:
                    utk.image(case_pos[0], case_pos[1],
                          "sprites/X.gif")

            # Affichage des cases explorer
            if "explore " in lvl.meanings[case]:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/magn_glass_" + lvl.meanings[case].replace("explore ", "") + ".gif")

            # Affichage des cases sabliers
            elif lvl.meanings[case] == "reinforcement unactivated":
                utk.image(case_pos[0], case_pos[1],
                          "sprites/reinforcement.gif")


    # Deuxième boucle identique à la première pour que les murs
    # soient chargés en dernier, au dessus des autres sprites
    for yy in range(1, len(lvl.level), 2):
        for xx in range(1, len(lvl.level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = lvl.level[yy][xx]  # Récupération de la valeur la case en question

            case_pos = (x * 40 + 20 + level_pos[0], y * 40 + 20 + level_pos[1])
            
            # Affichage des murs
            if lvl.meanings[case] == "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/wall.gif")


def display_command(x, y, size):
    utk.texte(x, y,
              """Déplacement : Z,Q,S,D
Sélection : B (pour changer), N (Pour verrouiller)
Mode Debug : F1""",
              taille=size)


def display_discuss(x, y):
    utk.image(win_size[0]/2, win_size[1]/2,
              "sprites/discuss.gif", 
              tag="discuss_icon")

    utk.texte(x, y, 
              "ENTREE pour \nreprendre...",
              ancrage="nw",
              taille=10,
              tag="discuss_info")

    display_frame()


def efface_discuss_icon():
    utk.efface("discuss_icon")

def efface_discuss():
    utk.efface("discuss_icon")
    utk.efface("discuss_info")


def display_escalators():
    for c_pos in lvl.escalator.keys():
        pair=(c_pos, lvl.escalator[c_pos])

        delta=((pair[1][0]-pair[0][0])//2, (pair[1][1]-pair[0][1])//2)
        if delta[1]>=0 and (delta[0]>=0 \
        or (delta[0]>=-2 and delta[1]>0)):
            utk.image(level_pos[0]+pair[0][0]//2*40+20, 
                      level_pos[1]+pair[0][1]//2*40+20,
                      "sprites/escalator/"+str(delta[0])+"_"+str(delta[1])+".gif")


def display_frame():
    if lvl.playing_loop:
        display_timer(x=0, y=0)
        display_selected_game()
        if lvl.has_stolen:
            open_exit()


def display_lose():
    utk.texte(win_size[0]/2, win_size[1]/2, 
              "Vous avez perdu...",
              couleur="red",
              ancrage="center",
              police="Purisa",
              taille=56)

    utk.mise_a_jour()


def display_pion(p):
    """
    Réaffiche le pion indiqué.
    :param int p: numéro du pion
    """
    utk.efface("pion"+str(p))
    name=lvl.pion_name[p]
    if "grenouille" in name:
        name="grenouille"
    utk.image(
        lvl.pion_pos[p][0]//2 * 40 + 20 + level_pos[0],
        lvl.pion_pos[p][1]//2 * 40 + 20 + level_pos[1],
        "sprites/" + name + ".gif",
        tag="pion"+str(p)
    )


def display_selected_game():
    """
    Affiche toutes les sélections en jeu.
    """
    for i in range(lvl.nbr_of_player):
        # Calcul des position d'affichage
        x = 5 + (level_pos[0] + level_px[0] + 20) * (i%2)
        y = 180 + 250 * (i>=2)

        # Affichage de la selection de pion
        pion_names = list(lvl.pion_name)
        select = lvl.selected_pion[i]
        for j in range(len(pion_names)):
            if "grenouille" in pion_names[j]:
                pion_names.pop(j)
                if select>j:
                    select-=1
                break
        if len(pion_names)>4:
            pion_n=[pion_names[j+select-1-len(pion_names)*(j+select-1>=len(pion_names))] for j in range(4)]
            display_selected_ingame(x, y, 
                                    select_value=1, 
                                    list_choice=pion_n, 
                                    tag_name="select_p"+str(i))
        else:
            display_selected_ingame(x, y, 
                                    select_value=select, 
                                    list_choice=pion_names, 
                                    tag_name="select_p"+str(i))

        # Affichage de la selection d'action
        #print("lvl.players_act", lvl.players_act)
        #print("lvl.nbr_of_player", lvl.nbr_of_player, i)
        if len(lvl.players_act[i])>4:
            select=lvl.selected_act[i]
            player_a=[lvl.players_act[i][j+select-1-len(lvl.players_act[i])*(j+select-1>=len(lvl.players_act[i]))] for j in range(4)]
            display_selected_ingame(x+50, y, 
                                    select_value=1, 
                                    list_choice=player_a, 
                                    tag_name="select_a"+str(i))
        else:
            display_selected_ingame(x+50, y, 
                                    select_value=lvl.selected_act[i], 
                                    list_choice=lvl.players_act[i], 
                                    tag_name="select_a"+str(i))

        # display_selected_ingame(x+50, y, lvl.selected_act[i], lvl.players_act[i], "select_a"+str(i)) POUBELLE


def display_selected_ingame(x, y, select_value, list_choice, tag_name="default"):
    """
    Affiche le pion sélectionné en jeu.
    """
    utk.efface(tag_name)

    utk.image(
        x+20, y+10,
        "sprites/select_arrow_up.gif",
        tag=tag_name)
    utk.image(
        x+20, y+len(list_choice)*40+30,
        "sprites/select_arrow_down.gif",
        tag=tag_name)

    for i in range(len(list_choice)):
        utk.rectangle(x, y+i*40+20, x+40, y+(i+1)*40+20,
                      couleur="black",
                      remplissage="cyan" * (i==select_value),
                      epaisseur=2,
                      tag=tag_name)
        utk.image(
            x+20, y+i*40+40,
            "sprites/" + list_choice[i] + ".gif",
            tag=tag_name)


def display_selected_target(pos_case):
    efface_selected_target()
    utk.image(
        pos_case[0]//2 * 40 + 20 + level_pos[0],
        pos_case[1]//2 * 40 + 20 + level_pos[1],
        "sprites/select_ingame.gif",
        tag="target_select"
    )

def efface_selected_target():
    utk.efface("target_select")


def display_timer(x, y):
    """
    Affiche le timer. Ne le met pas à jour.
    """
    utk.efface("timer")

    if timer.timer_paused:
        utk.image(x+50, y+50,
                  "sprites/hourglass_freeze.gif",
                  tag="timer")
    else:
        utk.image(x+50, y+50,
                  "sprites/hourglass.gif",
                  tag="timer")

    if timer.timer>0:
      utk.texte(x+50, y+110,
                str(int(timer.timer) // 60) + ":" + str(int(timer.timer % 60)),
                couleur="black",
                ancrage="center",
                police="Purisa",
                taille=28,
                tag="timer")
    else:
      utk.texte(x+50, y+110, 
                "0:0",
                couleur="black",
                ancrage="center",
                police="Purisa",
                taille=28,
                tag="timer")


def display_timer_X(case):
    pos_case=(level_pos[0]+40*(case[0]//2)+20, level_pos[1]+40*(case[1]//2)+20)
    utk.image(pos_case[0], pos_case[1],
              "sprites/X.gif", 
              tag="X_"+str(case[0])+"_"+str(case[1]))


def display_vortex(case_pos, meaning_case):
    """
    Affiche le vortex liée à la case et sa couleur.
    """
    sprite_name="sprites/"+meaning_case.replace(" ", "_")+".gif"
    utk.image(case_pos[0], case_pos[1],
              sprite_name)


def display_win():
    """
    Affiche 'Vous avez gagné !'
    """
    utk.texte(win_size[0]/2, win_size[1]/2, "Vous avez gagné !",
              couleur="lime",
              ancrage="center",
              police="Purisa",
              taille=56)
    utk.mise_a_jour()


def display_X_vortex():
    """
    Affiche la fermeture des vortex
    """
    for y in range(1, len(lvl.level), 2):
        for x in range(1, len(lvl.level[y]), 2):
            case = lvl.level[y][x]  # Récupération de la valeur la case en question

            if "vortex" in lvl.meanings[case]:
                # Centre de la position de la case en question
                case_pos = (x//2 * 40 + 20 + level_pos[0], y//2 * 40 + 20 + level_pos[1])
                utk.image(case_pos[0], case_pos[1],
                          "sprites/X.gif")


def init_game():
    """
    Charge la fenetre.
    """
    utk.cree_fenetre(win_size[0], win_size[1])


def open_exit():
    utk.efface("closed")
    utk.efface("to_steal")


#################### MENU ####################

def init_menu():
    """
    Initialise le menu
    """
    utk.rectangle(0, 0, win_size[0], win_size[1],
                  couleur="black",
                  remplissage="black",
                  epaisseur=1,
                  tag="background")


    utk.texte(win_size[0]/2, 60,"Magic-Maze",
              couleur="white",
              ancrage="center",
              police="Purisa",
              taille="40",
              tag="title")

    display_menu(0, ())


def init_pause():
    """
    Initialise le menu de pause.
    """
    utk.rectangle(200, 100, win_size[0]-200, win_size[1]-100,
                  couleur="black",
                  remplissage="grey",
                  epaisseur=5,
                  tag="background")

    display_pause(0, ("Reprendre", "Sauvegarder", "Quitter"))


def display_control():
    utk.image(win_size[0]//2, win_size[1]//2,
              "sprites/control.gif",
              tag="choice")


def display_pause(selected, menu_choice):
    """
    Affiche tout le menu.
    """
    display_pause_selection(selected)
    display_pause_choice(menu_choice)


def display_pause_choice(menu_choice):
    """
    Affiche les différents choix du menu.
    """
    utk.efface("choice")

    for i in range(len(menu_choice)):
        choice = menu_choice[i]

        if choice=="Nombre de joueur : ":
            choice+=str(lvl.nbr_of_player)

        utk.texte(win_size[0]/2, 120+i*40, choice,
                  couleur="black",
                  ancrage="center",
                  police="Purisa",
                  taille="16",
                  tag="choice")


def display_pause_selection(selected):
    """
    Affiche la sélection du menu
    """
    utk.efface("selection")

    utk.rectangle(win_size[0]/2-150, selected*40+105, win_size[0]/2+150, selected*40+135,
                  couleur="white",
                  remplissage="white",
                  epaisseur=1,
                  tag="selection")


def display_save_success():
    utk.texte(win_size[0]/2, win_size[1]-200, 
              "Sauvegarde terminé.",
              couleur="green",
              ancrage="center",
              police="Purisa",
              taille="16")


def display_menu(selected, menu_choice):
    """
    Affiche tout le menu.
    """
    display_menu_selection(selected)
    display_menu_choice(menu_choice)


def display_menu_choice(menu_choice):
    """
    Affiche les différents choix du menu.
    """
    utk.efface("choice")

    for i in range(len(menu_choice)):
        choice = menu_choice[i]

        if choice=="Nombre de joueur : ":
            choice+=str(lvl.nbr_of_player)

        utk.texte(win_size[0]/2, 120+i*40, choice,
                  couleur="white",
                  ancrage="center",
                  police="Purisa",
                  taille="16",
                  tag="choice")


def display_menu_selection(selected):
    """
    Affiche la sélection du menu
    """
    utk.efface("selection")

    utk.rectangle(win_size[0]/2-150, selected*40+105, win_size[0]/2+150, selected*40+135,
                  couleur="grey",
                  remplissage="grey",
                  epaisseur=1,
                  tag="selection")


