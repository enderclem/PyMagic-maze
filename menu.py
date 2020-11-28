# Contient les fonctions calculatoires.

import upemtk as utk
import levels as lvl
import display
import time
import timer

selected=0
nbr_choice=3

def main_menu(input):
    """
    Gère le menu principal.
    """
    global selected

    selected=change_selected(input, selected)
    change_nbr_player(input)    

    display.display_menu(selected)

    if confirm_play(input):
        lvl.menu_loop=False
        lvl.playing_loop=True
        timer.timer_paused=False

    elif confirm_exit(input):
        lvl.menu_loop=False


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
    if selected==0 and input=="Return":

        # Partage les actions entre les joueurs
        lvl.share_actions(lvl.nbr_of_player)

        display.display_all_level()

        return True

    return False

def confirm_exit(input):
    return selected==2 and input=="Return"