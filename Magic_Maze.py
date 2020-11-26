# Programme principal
from MagPy import *
import upemtk as utk
import doctest
import display
import levels as lvl
import random
import menu

in_menu = True
playing = True

def main():
    # Initialisation
    global in_menu, playing

    debug_mode = False
    all_input = ("z", "q", "s", "d", "b", "n", None)

    selection = 0

    display.init_game()
    display.init_menu()

    # Boucle du menu
    while in_menu:
        input = utk.attente_touche_jusqua(500)

        print(input)

        in_menu=menu.main_menu(input)

        exit_game(input)


    display.display_all_level()

    # Boucle de jeu
    while playing:
        input = utk.attente_touche_jusqua(20)

        exit_game(input)

        ##### Parti debug #####
        if input == "F1":
            debug_mode = not debug_mode
        if debug_mode:
            input = all_input[random.randint(0, len(all_input) - 1)]
        print(input)
        ##### Fin parti debug #####

        if input is not None:
            selection = selection_change(input, selection)
            move_player(input, selection)

        display.display_timer()
        check_steal()

        if check_exit() or update_time():
            break

    end_game()
    utk.ferme_fenetre()

def exit_game(input):
    global in_menu
    global playing

    if input == "Escape" or menu.confirm_exit(input):
        in_menu = False
        playing = False  # arret du programme



if __name__ == '__main__':
    main()
