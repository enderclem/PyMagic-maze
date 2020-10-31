# Contient toutes les fonctions d'affichages.

import upemtk as utk
from levels import *
import levels as lvl

win_scale_x = 600
win_scale_y = 500
win_level_pos = (0, 60)  # Donne la position du coin supérieur gauche de l'affichage du niveau

def display_all():
    """
    Réaffiche tous les éléments à la fenêtre.
    """
    global has_stole

    utk.efface_tout()
    # utk.rectangle(0, 0, win_scale_x, win_scale_y, remplissage="black")
    # utk.rectangle(0, 0, len(level[0]) * 40, len(level) * 40, remplissage="white")
    for y in range(len(level)):
        for x in range(len(level[y])):
            case = level[y][x]  # Récupération de la valeur la case en question

            # Centre de la position de la case en question
            case_pos = (x * 40 + 20 + win_level_pos[0], y * 40 + 20 + win_level_pos[1])

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

    display_selected(420, 10, 0, False)

    utk.mise_a_jour()


def display_lose():
    utk.texte(win_scale_x/2, win_scale_y/2, "Vous avez perdu...",
              ancrage="center")

    utk.mise_a_jour()


def display_player(p):
    """
    Réaffiche le pion indiqué.
    :param int p: numéro du pion
    """
    utk.efface(players_name[p])

    utk.image(
        players_pos[p][0] * 40 + 20 + win_level_pos[0],
        players_pos[p][1] * 40 + 20 + win_level_pos[1],
        "sprites/" + players_name[p] + ".gif",
        tag=players_name[p]
    )

    utk.mise_a_jour()


def display_selected(x, y, selected, is_blocked):
    utk.efface("selection")

    color_selected = ""
    if is_blocked:
        color_selected = "red"
    else:
        color_selected = "cyan"

    for i in range(4):
        utk.rectangle(x+i*40, y, x+(i+1)*40, y+40,
                      couleur="black",
                      remplissage=color_selected * (selected == i),
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
    utk.texte(win_scale_x/2, win_scale_y/2, "Vous avez gagné !",
              ancrage="center")

    utk.mise_a_jour()


def init_game():
    """
    Charge la fenetre et tout ce qui faut pour le jeu.
    """
    utk.cree_fenetre(win_scale_x, win_scale_y)
    display_all()


def open_exit():
    utk.efface("closed")

    utk.mise_a_jour()

