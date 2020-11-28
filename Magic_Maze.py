# Programme principal
from MagPy import *
import upemtk as utk
import doctest
import display
import levels as lvl
import random
import menu
import time
import timer

next_refresh = 0

def main():
    # Initialisation
    global in_menu, playing

    debug_mode = False
    all_input = ("a", "z", "q", "s", "w", "t", "g", "y", "h", "b")#, "a", "a", "a", "a", "a", "a", "a", "a", "a", "a")

    selection = 0

    display.init_game()
    display.init_menu()

    while True:

        input = utk.attente_touche_jusqua(100-80*debug_mode)
        print("input :", input)

        # Gestion du menu
        if lvl.menu_loop:
            menu.main_menu(input)
            timer.update_timer()

        # Gestion en jeu
        elif lvl.playing_loop:

            ##### Parti debug #####
            if input == "F1":
                debug_mode = not debug_mode
            if debug_mode:
                input = all_input[random.randint(0, len(all_input) - 1)]
            ##### Fin parti debug #####

            if input is not None:
                player_choose(input)

            timer.update_timer()
            check_steal()

            refresh_display()

        display.display_frame()
        utk.mise_a_jour()

        if check_exit() or timer.timer<=0:
            break

        if input == "Escape":
            break

    end_game()
    utk.ferme_fenetre()



def refresh_display():
    """
    Reinitialise l'affichage du jeu pour éviter un certain bug.
    """
    global next_refresh
    if time.process_time()>next_refresh:
        next_refresh+=30
        display.display_all_level()


if __name__ == '__main__':
    main()
