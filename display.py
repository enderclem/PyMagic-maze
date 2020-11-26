# Contient toutes les fonctions d'affichages.

import upemtk as utk
from levels import * # Importation en double à régler
import levels as lvl

win_size = (900, 720)
level_pos = (0, 60)  # Donne la position du coin supérieur gauche de l'affichage du niveau
level_size = (900, 600)

def display_all_level():
    """
    Réaffiche tous les éléments à la fenêtre.
    """
    global has_stole

    utk.efface_tout()

    utk.rectangle(level_pos[0], level_pos[1], 
                  level_pos[0]+level_size[0], level_pos[1]+level_size[1],
                  couleur="black",
                  remplissage="black",
                  epaisseur=0,
                  tag="background")

    display_cases()
    display_between_cases()

    for i in range(4):
        display_player(i)
    display_selected(420, 10, 0)
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
            if "to steal" in meanings[case]:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/stuff_" + meanings[case].replace("to steal ", "") + ".gif")

            # Affichage des sorties
            elif "exit" in meanings[case]:
                utk.image(case_pos[0], case_pos[1],
                          "sprites/exit_" + meanings[case].replace("exit ", "") + ".gif")

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


def display_lose():
    utk.texte(win_size[0]/2, win_size[1]/2, "Vous avez perdu...",
              ancrage="center")

    utk.mise_a_jour()


def display_player(p):
    """
    Réaffiche le pion indiqué.
    :param int p: numéro du pion
    """
    utk.efface(players_name[p])

    utk.image(
        players_pos[p][0]//2 * 40 + 20 + level_pos[0],
        players_pos[p][1]//2 * 40 + 20 + level_pos[1],
        "sprites/" + players_name[p] + ".gif",
        tag=players_name[p]
    )

    utk.mise_a_jour()


def display_selected(x, y, selected):
    utk.efface("selection")

    for i in range(4):
        utk.rectangle(x+i*40, y, x+(i+1)*40, y+40,
                      couleur="black",
                      remplissage="cyan" * (i==selected),
                      epaisseur=2,
                      tag="selection")
        utk.image(
            x+i*40+20, y+20,
            "sprites/" + players_name[i] + ".gif",
            tag="selection")

    utk.mise_a_jour()


def display_timer():
    utk.efface("timer")
    utk.texte(300, 15, "temps restants",
              couleur="black",
              ancrage="center",
              police="Purisa",
              taille="20",
              tag="timer")
    utk.texte(300, 45,str(int(lvl.time_left) // 60) + "min" + str(int(lvl.time_left % 60)) + "s",
              couleur="black",
              ancrage="center",
              police="Purisa",
              taille="20",
              tag="timer")

    utk.mise_a_jour()


def display_win():
    utk.texte(win_size[0]/2, win_size[1]/2, "Vous avez gagné !",
              ancrage="center")

    utk.mise_a_jour()


def init_game():
    """
    Charge la fenetre et tout ce qui faut pour le jeu.
    """
    utk.cree_fenetre(win_size[0], win_size[1])


def open_exit():
    utk.efface("closed")

    utk.mise_a_jour()



#################### MENU ####################

def init_menu():
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

def display_menu(selected):
    display_menu_selection(selected)
    display_choice()

def display_choice():
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
    utk.efface("selection")

    utk.rectangle(win_size[0]/2-150, selected*40+105, win_size[0]/2+150, selected*40+135,
                  couleur="grey",
                  remplissage="grey",
                  epaisseur=1,
                  tag="selection")


