# Contient les fonctions calculatoires.

import upemtk as utk
import levels as lvl
import display
import time

selected=0
nbr_choice=3

def main_menu(input):
    """
    Retourne True tant que le menu est sensé s'afficher.
    """
    global selected

    selected=change_selected(input, selected)
    change_nbr_player(input)    

    display.display_menu(selected)

    return not confirm_play(input)

def change_selected(input, selected):
    """
    Change la selection.
    """
    if input=="Up":
        selected-=1
        if selected < 0:
            selected=0
        print(selected)

    elif input=="Down":
        selected+=1
        if selected >= nbr_choice:
            selected=nbr_choice-1
        print(selected)

    return selected

def change_nbr_player(input):
    if selected==1:
        if input=="Left":
            lvl.nbr_of_player-=1
            if lvl.nbr_of_player<=0:
                lvl.nbr_of_player=1
        if input=="Right":
            lvl.nbr_of_player+=1
            if lvl.nbr_of_player>4:
                lvl.nbr_of_player=4
    

def confirm_play(input):
    return selected==0 and input=="Return"

def confirm_exit(input):
    return selected==2 and input=="Return"