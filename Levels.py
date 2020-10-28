# fichier pour gérer la génération du niveau

# Variables contenant les collisions du niveau:
#   - 0 : la case est vide;
#   - 1 : la case est un mur plein;
#   - 2 : la case est occupée par un personnage.
#	- 3 : la case est la sortie associée au joueur 1
#	- 4 : la case est la sortie associée au joueur 2
#	- 5 : la case est la sortie associée au joueur 3
#	- 6 : la case est la sortie associée au joueur 4
level = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 1, 0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
