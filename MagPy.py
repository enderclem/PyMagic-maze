# On définit les fonctions ici.
import upemtk as utk

win_scale_x = 0
win_scale_y = 0

def init_game(window_scale_x, window_scale_y):
    """
    Charge la fenetre et tout ce qui faut pour le jeu.
    """
    global win_scale_x
    global win_scale_y
    utk.cree_fenetre(window_scale_x, window_scale_y)
    win_scale_x = window_scale_x
    win_scale_y = window_scale_y

def issou():
    """
    Hehehe
    """
    utk.image(win_scale_x // 2, win_scale_y // 2, "issou.gif")


