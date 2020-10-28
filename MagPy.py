# On définit les fonctions ici.
import upemtk as utk
from Levels import level, meanings

win_scale_x = 600
win_scale_y = 400
players_name = ("magicienne", "elfe", "nain", "barbare")
players_pos = [(6, 4), (6, 5), (7, 4), (7, 5)]
players_input = ("z", "s", "q", "d")

selection_blocked = False


def display():
    """
    Réaffiche tous les éléments à la fenêtre.
    """
    utk.efface_tout()
    utk.rectangle(0, 0, win_scale_x, win_scale_y, remplissage="black")
    utk.rectangle(0, 0, len(level[0]) * 40, len(level) * 40, remplissage="white")
    for y in range(len(level)):
        for x in range(len(level[y])):
            case = level[y][x]  # Récupération de la valeur la case en question
            case_pos = (x * 40 + 20, y * 40 + 20)  # Centre de la position de la case en question
            if meanings[case] is None:
                pass # Mettre une image à afficher pour le sol
            elif meanings[case] == "wall":
                utk.rectangle(case_pos[0] - 20, case_pos[1] - 20, case_pos[0] + 20, case_pos[1] + 20,
                              remplissage="gray", epaisseur=0)
            elif "to steal" in meanings[case]:
                utk.image(case_pos[0], case_pos[1], "sprites/stuff_" + meanings[case].replace("to steal ", "") + ".gif")

    for i in range(4):
        utk.image(
            players_pos[i][0] * 40 + 20,
            players_pos[i][1] * 40 + 20,
            "sprites/" + players_name[i] + ".gif")


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
    pla = players_pos[p]  # Création d'un raccourci pour appeler la position du personnage

    vec_move_x = (touche == players_input[3]) - (touche == players_input[2])
    vec_move_y = (touche == players_input[1]) - (touche == players_input[0])
    new_pos = (pla[0] + vec_move_x, pla[1] + vec_move_y)

    if -1 < new_pos[1] < len(level) and -1 < new_pos[0] < len(level[0]) \
            and level[new_pos[1]][new_pos[0]] != "w" \
            and new_pos not in players_pos:
        players_pos[p] = new_pos


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
