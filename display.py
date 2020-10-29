# Contient toutes les fonctions d'affichages.

import upemtk as utk
from levels import *

win_scale_x = 600
win_scale_y = 400

def display_all():
    """
    Réaffiche tous les éléments à la fenêtre.
    """
    global has_stole

    utk.efface_tout()
    utk.rectangle(0, 0, win_scale_x, win_scale_y, remplissage="black")
    utk.rectangle(0, 0, len(level[0]) * 40, len(level) * 40, remplissage="white")
    for y in range(len(level)):
        for x in range(len(level[y])):
            case = level[y][x]  # Récupération de la valeur la case en question
            case_pos = (x * 40 + 20, y * 40 + 20)  # Centre de la position de la case en question

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
                print(meanings[case])
                utk.image(case_pos[0], case_pos[1],
                          "sprites/X.gif",
                          tag="closed")

            # Affichage des murs
            if meanings[case] == "wall":
                utk.rectangle(case_pos[0] - 20, case_pos[1] - 20, case_pos[0] + 20, case_pos[1] + 20,
                              remplissage="gray", epaisseur=0)

    for i in range(4):
        display_player(i)


def display_player(p):
    """
    Réaffiche le pion indiqué.
    :param int p: numéro du pion
    """
    utk.efface(players_name[p])

    utk.image(
        players_pos[p][0] * 40 + 20,
        players_pos[p][1] * 40 + 20,
        "sprites/" + players_name[p] + ".gif",
        tag=players_name[p]
    )


def display_timer():
    pass

def display_win():
    utk.texte(win_scale_x/2, win_scale_y/2, "Vous avez gagné !",
              ancrage="center")

def init_game():
    """
    Charge la fenetre et tout ce qui faut pour le jeu.
    """
    utk.cree_fenetre(win_scale_x, win_scale_y)
    display_all()


def open_exit():
    utk.efface("closed")
