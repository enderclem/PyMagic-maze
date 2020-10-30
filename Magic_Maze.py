# Programme principal
from MagPy import *
import upemtk as utk
import doctest
import display
import levels as lvl

def main():
    selection = 0

    display.init_game()

    playing = True
    while playing:
        input = utk.attente_touche(100)
        # print(input)

        if input is not None:
            if input == "Escape":
                playing = False  # arret du programme
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
