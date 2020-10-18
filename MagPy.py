# On définit les fonctions ici.
import upemtk as utk
from Levels import level

win_scale_x = 600
win_scale_y = 400
player_pos = (2, 2)

def display():
    utk.efface_tout()
    utk.rectangle(0, 0, win_scale_x, win_scale_y, remplissage="black")
    utk.rectangle(0, 0, len(level[0]) * 40, len(level) * 40, remplissage="white")
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 1:
                utk.rectangle(x*40, y*40, (x+1)*40, (y+1)*40, remplissage="gray", epaisseur=0)

    utk.cercle(player_pos[0]*40+20, player_pos[1]*40+20, 15, remplissage="purple", epaisseur=2)



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

def move_player(touche):
    """
    Bouge le joueur selon la touche indiquée.
    """
    global player_pos
    vec_move_x = (touche == "d") - (touche == "q")
    vec_move_y = (touche == "s") - (touche == "z")
    new_pos = (player_pos[0] + vec_move_x, player_pos[1] + vec_move_y)

    if -1<new_pos[1]<len(level) and -1<new_pos[0]<len(level[0]) and level[new_pos[1]][new_pos[0]] not in (1, 2):
        level[player_pos[1]][player_pos[0]] = 0
        level[new_pos[1]][new_pos[0]] = 2
        player_pos = new_pos
