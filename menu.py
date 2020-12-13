# Contient les fonctions calculatoires.

import upemtk as utk
import levels as lvl
import display
import time
import timer

selected=0
nbr_choice=3
paused=False

menu_sel=0

menu_choice=(
    ("Jouer", "Nombre de joueur : ", "Commandes", "Quitter"),
    ("Continuer", "Nouvelle partie", "Retour"),
    ("Retour",),
    ("Reprendre", "Sauvegarder", "Quitter"))


main_val=0
play_val=1
commands_val=2
pause_val=3

def main_menu(input):
    """
    Gère le menu principal.
    """
    global selected, menu_sel, menu_choice
    global main_val, play_val, commands_val

    selected=change_selected(input, selected)

    #Choix du menu
    if menu_sel==main_val:
        choice=menu_choice[main_val][selected]
        change_nbr_player(input)
        if input=="Return":
            if choice=="Jouer":
                print("ok")
                menu_sel=play_val
                selected=0

            if choice=="Commandes":
                menu_sel=commands_val
                selected=0

            if choice=="Quitter":
                lvl.menu_loop=False


    elif menu_sel==play_val:
        choice=menu_choice[play_val][selected]
        if input=="Return":
            if choice=="Continuer":
                load_game()

            if choice=="Nouvelle partie":
                new_game()

            if choice=="Retour":
                menu_sel=main_val
                selected=0

    elif menu_sel==commands_val:
        choice=menu_choice[commands_val][selected]
        if input=="Return":
            if choice=="Retour":
                menu_sel=main_val
                selected=0


    # Affichage
    if lvl.playing_loop==True:
        display.display_all_level()
    else:
        display.display_menu(selected,
                             menu_choice[menu_sel])


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
        if selected >= len(menu_choice[menu_sel]):
            selected=len(menu_choice[menu_sel])-1

    return selected


def change_nbr_player(input):
    if menu_choice[main_val][selected]=="Nombre de joueur : ":
        if input=="Left":
            lvl.nbr_of_player-=1
            if lvl.nbr_of_player<=0:
                lvl.nbr_of_player=1
        if input=="Right":
            lvl.nbr_of_player+=1
            if lvl.nbr_of_player>4:
                lvl.nbr_of_player=4
    

def new_game():
    global selected
    lvl.menu_loop=False
    lvl.playing_loop=True
    timer.timer_paused=False
    lvl.load_new_level(display.level_px[0]//40, display.level_px[1]//40)
    selected=0


def load_game():
    global selected
    lvl.menu_loop=False
    lvl.playing_loop=True
    timer.timer_paused=False
    selected=0
    timer.set_timer(lvl.load_game())


def pause_menu(input):
    global selected, menu_sel, menu_choice
    global pause_val

    selected=change_selected(input, selected)
    stop_pause=False

    if menu_sel==pause_val:
        choice=menu_choice[pause_val][selected]
        change_nbr_player(input)
        if input=="Return":
            if choice=="Reprendre":
                stop_pause=True

            if choice=="Sauvegarder":
                lvl.save_game(timer.timer)
                display.display_save_success()

            if choice=="Quitter":
                lvl.playing_loop=False

    display.display_pause(selected, menu_choice[menu_sel])

    if stop_pause:
        quit_pause_menu()


def activate_pause_menu():
    global paused, menu_sel
    paused=True
    timer.timer_paused=True
    menu_sel=pause_val
    display.init_pause()


def quit_pause_menu():
    global paused
    paused=False
    timer.timer_paused=False
    display.display_all_level()



