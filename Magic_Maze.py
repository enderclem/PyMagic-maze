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
    all_input = ("a", "z", "q", "s", "w", "t", "g", "y", "h", "b", "colon", "o", "l", "p", "m", "8", "5", "9", "6", "2", "Up", "Down", "Left", "Right", "Return")

    selection = 0

    display.init_game()
    display.init_menu()

    while True:

        input = utk.attente_touche_jusqua(100-100*debug_mode)

        # Gestion du menu
        if lvl.menu_loop:
            print("input :", input)
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
            print("input :", input)

            if input is not None:
                if lvl.discussing:
                    lvl.discussing=False
                    display.efface_discuss()
                elif lvl.player_using_vortex!=-1:
                    vortex_selection(input)
                elif lvl.player_using_spell!=-1:
                    spell_target_selection(input)
                elif menu.paused==True:
                    menu.pause_menu(input)
                else:
                    player_choose(input)
                    check_steal(input)
                    if input == "Escape":
                        print("affichage du menu pause")
                        menu.activate_pause_menu()

            timer.update_timer()
            check_steal()

        refresh_display()
        display.display_frame()
        utk.mise_a_jour()

        if check_exit() or check_timer() or (lvl.playing_loop and check_guard_catch()) \
        or input == "F4" or (not lvl.menu_loop and not lvl.playing_loop):
            break

    end_game()
    utk.ferme_fenetre()


def refresh_display():
    """
    Reinitialise l'affichage du jeu pour éviter un certain bug.
    """
    global next_refresh
    if time.process_time()>next_refresh and lvl.playing_loop: # and not menu.paused:
        while time.process_time()>next_refresh:
            next_refresh+=20
        display.display_all_level()
        if menu.paused:
            display.init_pause()
            display.display_pause(menu.selected, menu.menu_choice[menu.menu_sel])


if __name__ == '__main__':
    main()
