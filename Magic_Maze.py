# Programme principal
from MagPy import *
import upemtk as utk
import doctest

def main():
    init_game()

    playing = True
    while playing:
        input = utk.attente_clic_ou_touche()
        print(input)

        if input[2] == "Touche":
            if input[1] == "Escape":
                # arret du programme
                playing = False
            if input[1] in ("z", "q", "s", "d"):
                move_player(input[1])

        display()
        if input[2] == "ClicGauche":
            issou()


    utk.ferme_fenetre()


if __name__ == '__main__':

    main()