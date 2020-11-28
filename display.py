# Contient toutes les fonctions d'affichages.

import upemtk as utk
from levels import * # Importation en double à régler
import levels as lvl
import timer

win_size = (1200, 680)
level_pos = (120, 20)  # Donne la position du coin supérieur gauche de l'affichage du niveau
level_size = (960, 640)

def display_all_level():
    """
    Réaffiche tous les éléments à la fenêtre.
    """
    global has_stole

    utk.efface_tout()

    utk.rectangle(level_pos[0]-20, level_pos[1]-20, 
                  level_pos[0]+level_size[0]+20, level_pos[1]+level_size[1]+20,
                  couleur="black",
                  remplissage="black",
                  epaisseur=0,
                  tag="background")

    display_cases()
    display_between_cases()

    for i in range(4):
        display_player(i)
    display_selected_game()
    display_command(10, 460, 12)

    utk.mise_a_jour()

def display_between_cases():

    for yy in range(0, len(level), 2):
        for xx in range(1, len(level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = level[yy][xx]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + 20 + level_pos[0], y * 40 + level_pos[1])

            # Affichage des murs
            if meanings[case] == "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/wall_horizontal.gif")

    for yy in range(1, len(level), 2):
        for xx in range(0, len(level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = level[yy][xx]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + level_pos[0], y * 40 + 20 + level_pos[1])

            # Affichage des murs
            if meanings[case] == "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/wall_vertical.gif")


def display_cases():
    for yy in range(1, len(level), 2):
        for xx in range(1, len(level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = level[yy][xx]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + 20 + level_pos[0], y * 40 + 20 + level_pos[1])

            # Affichage du sol
            if meanings[case] != "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/ground.gif")

            # Affichage des zones à voler
            if "to steal" in meanings[case] and not lvl.has_stolen:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/stuff_" + meanings[case].replace("to steal ", "") + ".gif", 
                          tag="to_steal")

            # Affichage des sorties
            elif "exit" in meanings[case]:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/exit_" + meanings[case].replace("exit ", "") + ".gif")

                if not lvl.has_stolen:
                    utk.image(case_pos[0], case_pos[1],
                              "sprites/X.gif",
                              tag="closed")

    # Deuxième boucle identique à la première pour que les murs
    # soient chargés en dernier, au dessus des autres sprites
    for yy in range(1, len(level), 2):
        for xx in range(1, len(level[yy]), 2):
            y=yy//2 # Calcul du numéro de la case
            x=xx//2
            case = level[yy][xx]  # Récupération de la valeur la case en question

            case_pos = (x * 40 + 20 + level_pos[0], y * 40 + 20 + level_pos[1])
            
            # Affichage des murs
            if meanings[case] == "wall":
                utk.image(case_pos[0], case_pos[1], "sprites/wall.gif")


def display_command(x, y, size):
    utk.texte(x, y,
              """Déplacement : Z,Q,S,D
Sélection : B (pour changer), N (Pour verrouiller)
Mode Debug : F1""",
              taille=size)

def display_frame():
    if lvl.playing_loop:
        for i in range(4):
            display_player(i)

        display_timer(x=0, y=0)
        display_selected_game()
        if lvl.has_stolen:
            open_exit()


def display_lose():
    utk.texte(win_size[0]/2, win_size[1]/2, "Vous avez perdu...",
              ancrage="center")

    utk.mise_a_jour()


def display_player(p):
    """
    Réaffiche le pion indiqué.
    :param int p: numéro du pion
    """
    utk.efface(pion_name[p])

    utk.image(
        pion_pos[p][0]//2 * 40 + 20 + level_pos[0],
        pion_pos[p][1]//2 * 40 + 20 + level_pos[1],
        "sprites/" + pion_name[p] + ".gif",
        tag=pion_name[p]
    )


def display_selected_game():
    """
    Affiche toutes les sélections en jeu.
    """
    for i in range(lvl.nbr_of_player):
        # Calcul des position d'affichage
        x = 5 + (level_pos[0] + level_size[0] + 20) * (i%2)
        y = 180 + 250 * (i>=2)
        
        display_selected_pion(x, y, lvl.selected_pion[i], i)
        display_selected_action(x+50, y, lvl.selected_act[i], lvl.players_act[i], i)


def display_selected_pion(x, y, select_value, player_num=-1):
    """
    Affiche le pion sélectionné en jeu.
    """
    tag_name="select_p" + str(player_num)
    utk.efface(tag_name)

    for i in range(4):
        utk.rectangle(x, y+i*40, x+40, y+(i+1)*40,
                      couleur="black",
                      remplissage="cyan" * (i==select_value),
                      epaisseur=2,
                      tag=tag_name)
        utk.image(
            x+20, y+i*40+20,
            "sprites/" + pion_name[i] + ".gif",
            tag=tag_name)


def display_selected_action(x, y, select_value, list_actions, player_num=-1):
    """
    Affiche le pion sélectionné en jeu.
    """
    tag_name="select_a" + str(player_num)
    utk.efface(tag_name)

    for i in range(len(list_actions)):
        utk.rectangle(x, y+i*40, x+40, y+(i+1)*40,
                      couleur="black",
                      remplissage="cyan" * (i==select_value),
                      epaisseur=2,
                      tag=tag_name)
        utk.image(
            x+20, y+i*40+20,
            "sprites/" + list_actions[i] + ".gif",
            tag=tag_name)


def display_timer(x, y):
    """
    Affiche le timer. Ne le met pas à jour.
    """
    utk.efface("timer")

    utk.image(x+50, y+50,
              "sprites/hourglass.gif",
              tag="timer")
    utk.texte(x+50, y+110,str(int(timer.timer) // 60) + ":" + str(int(timer.timer % 60)),
              couleur="black",
              ancrage="center",
              police="Purisa",
              taille=28,
              tag="timer")


def display_win():
    """
    Affiche 'Vous avez gagné !'
    """
    utk.texte(win_size[0]/2, win_size[1]/2, "Vous avez gagné !",
              ancrage="center")

    utk.mise_a_jour()


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

    display_menu(0)

def display_menu(selected):
    """
    Affiche tout le menu.
    """
    display_menu_selection(selected)
    display_choice()

def display_choice():
    """
    Affiche les différents choix du menu.
    """
    utk.efface("choice")

    utk.texte(win_size[0]/2, 120,"Commencer",
              couleur="white",
              ancrage="center",
              police="Purisa",
              taille="16",
              tag="choice")
    utk.texte(win_size[0]/2, 160,"Nombre de joueur : " + str(lvl.nbr_of_player),
              couleur="white",
              ancrage="center",
              police="Purisa",
              taille="16",
              tag="choice")
    utk.texte(win_size[0]/2, 200,"Quitter",
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


