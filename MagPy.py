# On définit les fonctions ici.
import upemtk as utk
from Levels import level

win_scale_x = 600
win_scale_y = 400
player_pos1 = (4, 4)
player_pos2 = (4, 5)
player_pos3 = (5, 4)
player_pos4 = (5, 5)

def display():
    utk.efface_tout()
    utk.rectangle(0, 0, win_scale_x, win_scale_y, remplissage="black")
    utk.rectangle(0, 0, len(level[0]) * 40, len(level) * 40, remplissage="white")
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 1:
                utk.rectangle(x*40, y*40, (x+1)*40, (y+1)*40, remplissage="gray", epaisseur=0)

    utk.cercle(player_pos1[0]*40+20, player_pos1[1]*40+20, 15, remplissage="purple", epaisseur=2)
    utk.cercle(player_pos2[0]*40+20, player_pos2[1]*40+20, 15, remplissage="green", epaisseur=2)
    utk.cercle(player_pos3[0]*40+20, player_pos3[1]*40+20, 15, remplissage="orange", epaisseur=2)
    utk.cercle(player_pos4[0]*40+20, player_pos4[1]*40+20, 15, remplissage="yellow", epaisseur=2)



def init_game():
    """
    Charge la fenetre et tout ce qui faut pour le jeu.
    """
    utk.cree_fenetre(win_scale_x, win_scale_y)
    display()

def issou():
    """
    Hehehe boy
    """
    utk.efface_tout()
    utk.image(win_scale_x // 2, win_scale_y // 2, "issou.gif")

def move_player1(touche):
    """
    Bouge le joueur 1 selon la touche indiquée.
    """
    global player_pos1
    vec_move_x = (touche == "d") - (touche == "q")
    vec_move_y = (touche == "s") - (touche == "z")
    new_pos = (player_pos1[0] + vec_move_x, player_pos1[1] + vec_move_y)

    if -1<new_pos[1]<len(level) and -1<new_pos[0]<len(level[0]) and level[new_pos[1]][new_pos[0]] not in (1, 2):
        level[player_pos1[1]][player_pos1[0]] = 0
        level[new_pos[1]][new_pos[0]] = 2
        player_pos1 = new_pos

def move_player2(touche):
    """
    Bouge le joueur 2 selon la touche indiquée.
    """
    global player_pos2
    vec_move_x = (touche == "m") - (touche == "k")
    vec_move_y = (touche == "l") - (touche == "o")
    new_pos = (player_pos2[0] + vec_move_x, player_pos2[1] + vec_move_y)

    if -1<new_pos[1]<len(level) and -1<new_pos[0]<len(level[0]) and level[new_pos[1]][new_pos[0]] not in (1, 2):
        level[player_pos2[1]][player_pos2[0]] = 0
        level[new_pos[1]][new_pos[0]] = 2
        player_pos2 = new_pos

def move_player3(touche):
    """
    Bouge le joueur 3 selon la touche indiquée.
    """
    global player_pos3
    vec_move_x = (touche == "Right") - (touche == "Left")
    vec_move_y = (touche == "Down") - (touche == "Up")
    new_pos = (player_pos3[0] + vec_move_x, player_pos3[1] + vec_move_y)

    if -1<new_pos[1]<len(level) and -1<new_pos[0]<len(level[0]) and level[new_pos[1]][new_pos[0]] not in (1, 2):
        level[player_pos3[1]][player_pos3[0]] = 0
        level[new_pos[1]][new_pos[0]] = 2
        player_pos3 = new_pos

def move_player4(touche):
    """
    Bouge le joueur 4 selon la touche indiquée.
    """
    global player_pos4
    vec_move_x = (touche == "6") - (touche == "4")
    vec_move_y = (touche == "5") - (touche == "8")
    new_pos = (player_pos4[0] + vec_move_x, player_pos4[1] + vec_move_y)

    if -1<new_pos[1]<len(level) and -1<new_pos[0]<len(level[0]) and level[new_pos[1]][new_pos[0]] not in (1, 2):
        level[player_pos4[1]][player_pos4[0]] = 0
        level[new_pos[1]][new_pos[0]] = 2
        player_pos4 = new_pos

