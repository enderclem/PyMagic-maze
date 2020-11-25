# Programme principal
from MagPy import *
import upemtk as utk
import doctest
import display
import levels as lvl
import random

def main():
    debug_mode = False
    all_input = ("z", "q", "s", "d", "b", "n", None)

    selection = 0

    display.init_game()

    playing = True
    while playing:
        input = utk.attente_touche_jusqua(10)

        if input == "Escape":
            playing = False  # arret du programme

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


if __name__ == '__main__':
    main()
