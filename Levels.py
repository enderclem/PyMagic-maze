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
    "ww----wwww---ww",
    "w(-w--w--w---)w",
    "www--ww-w----ww",
    "----ww$-ww---w@",
    "---------w---w-",
    "----w-------w--",
    "----ww--ww--w-w",
    "----£w-ww-----w",
    "w]--€w-------[w",
    "ww-----------ww",
]

meanings = {
    "-": None,
    "w": "wall",
    "c": "character",
    "$": "to steal magicienne",
    "£": "to steal elfe",
    "€": "to steal nain",
    "@": "to steal barbare",
    "(": "exit magicienne",
    ")": "exit elfe",
    "[": "exit nain",
    "]": "exit barbare",
}
