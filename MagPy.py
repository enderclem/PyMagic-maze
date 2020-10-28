# On définit les fonctions ici.
import upemtk as utk
from Levels import level

win_scale_x = 600
win_scale_y = 400
players = [
    (4, 4),
    (4, 5),
    (5, 4),
    (5, 5),
]
players_input = ("z", "s", "q", "d")


selection_blocked = False

def display():
    utk.efface_tout()
    utk.rectangle(0, 0, win_scale_x, win_scale_y, remplissage="black")
    utk.rectangle(0, 0, len(level[0]) * 40, len(level) * 40, remplissage="white")
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 1:
                utk.rectangle(x * 40 + 2, y * 40 + 2, (x + 1) * 40 - 2, (y + 1) * 40 - 2, remplissage="gray",
                              epaisseur=0)

    for i in range(4):
        utk.image(
            players[i][0] * 40 + 20, players[i][1] * 40 + 20,
                  "sprites/magicienne.gif" * (i==0) +
                  "sprites/elfe.gif" * (i==1) +
                  "sprites/nain.gif" * (i==2) +
                  "sprites/barbare.gif" * (i==3)
                  )

def init_game():
    """
    Charge la fenetre et tout ce qui faut pour le jeu.
    """
    win = utk.cree_fenetre(win_scale_x, win_scale_y)
    display()


def move_player(touche, p):
    """
    Bouge le joueur 1 selon la touche indiquée.

    :param string touche: touche du clavier appuyé
    :param int p: numéro du joueur
    """
    global players
    global players_input
    pla = players[p] # Création d'un raccourci pour appeler la position du personnage

    vec_move_x = (touche == players_input[3]) - (touche == players_input[2])
    vec_move_y = (touche == players_input[1]) - (touche == players_input[0])
    new_pos = (pla[0] + vec_move_x, pla[1] + vec_move_y)

    if -1 < new_pos[1] < len(level) and -1 < new_pos[0] < len(level[0]) and level[new_pos[1]][new_pos[0]] not in (1, 2):
        level[pla[1]][pla[0]] = 0
        level[new_pos[1]][new_pos[0]] = 2
        players[p] = new_pos


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
